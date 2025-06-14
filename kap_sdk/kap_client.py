import os
import tempfile
import logging
from datetime import datetime, timedelta
import requests
import diskcache
from typing import Optional, List, Dict, Any
from kap_sdk.models.announcement_type import AnnouncementType, FundType, MemberType
from kap_sdk.models.company import Company, scrape_companies
from kap_sdk.models.indices import Indice, scrape_indices
from kap_sdk.models.company_info import CompanyInfo, scrape_company_info
from kap_sdk.models.sectors import Sector, scrape_sectors
from kap_sdk._financial_report import get_financial_report
from kap_sdk._search_oid import _search_oid
from kap_sdk.models.disclosure import Disclosure, DisclosureBasic, DisclosureDetail

_CACHE_DIR = os.path.join(tempfile.gettempdir(), "kap_cache_v3")
os.makedirs(_CACHE_DIR, exist_ok=True)

class KapClient:
    def __init__(
        self,
        cache_expiry: int = 3600,
        company_cache_expiry: int = 86400,
        indices_cache_expiry: int = 86400,
        sectors_cache_expiry: int = 86400
    ):
        self.cache = diskcache.Cache(_CACHE_DIR)
        self.cache_expiry = cache_expiry
        self.company_cache_expiry = company_cache_expiry
        self.indices_cache_expiry = indices_cache_expiry
        self.sectors_cache_expiry = sectors_cache_expiry
        logging.info("KapClient initialized with custom cache expiry settings.")

    async def get_companies(self, fetch_remote: bool = False) -> List[Company]:
        key = "companies"
        if not fetch_remote:
            cached_companies = self.cache.get(key=key)
            if cached_companies:
                logging.info("Returning cached companies list.")
                return [Company(**company) for company in cached_companies]
        try:
            companies = await scrape_companies()
            self.cache.set(key, [company.dict() for company in companies], expire=self.company_cache_expiry)
            logging.info(f"Scraped and cached {len(companies)} companies.")
            return companies
        except Exception as e:
            logging.error(f"Error scraping companies: {e}")
            raise

    async def get_indices(self, fetch_remote: bool = False) -> List[Indice]:
        key = "indices"
        if not fetch_remote:
            cached_indices = self.cache.get(key=key)
            if cached_indices:
                logging.info("Returning cached indices list.")
                return [Indice(**indice) for indice in cached_indices]
        try:
            indices = await scrape_indices()
            self.cache.set(key, [indice.dict() for indice in indices], expire=self.indices_cache_expiry)
            logging.info(f"Scraped and cached {len(indices)} indices.")
            return indices
        except Exception as e:
            logging.error(f"Error scraping indices: {e}")
            raise

    async def get_company(self, code: str) -> Optional[Company]:
        companies = await self.get_companies()
        for company in companies:
            if company.code == code:
                logging.info(f"Found company with code {code}.")
                return company
        logging.warning(f"Company with code {code} not found.")
        return None

    async def get_indice(self, code: str) -> Optional[Indice]:
        indices = await self.get_indices()
        for indice in indices:
            if indice.code == code:
                logging.info(f"Found indice with code {code}.")
                return indice
        logging.warning(f"Indice with code {code} not found.")
        return None

    async def get_company_info(self, company: Company, fetch_remote: bool = False) -> Optional[CompanyInfo]:
        key = f"infos_{company.code}"
        if not fetch_remote:
            cached_company_info = self.cache.get(key=key)
            if cached_company_info:
                logging.info(f"Returning cached company info for {company.code}.")
                return CompanyInfo(**cached_company_info)
        try:
            company_info = await scrape_company_info(company)
            self.cache.set(key, company_info.dict(), expire=self.cache_expiry)
            logging.info(f"Scraped and cached company info for {company.code}.")
            return company_info
        except Exception as e:
            logging.error(f"Error scraping company info for {company.code}: {e}")
            raise

    async def get_financial_report(self, company: Company, year: str = "2023", fetch_remote: bool = False) -> Dict[str, Any]:
        key = f"financial_report_{company.code}_{year}"
        if not fetch_remote:
            cached_financial_report = self.cache.get(key=key)
            if cached_financial_report:
                logging.info(f"Returning cached financial report for {company.code}, year {year}.")
                return cached_financial_report
        try:
            financial_report = await get_financial_report(company=company, year=year)
            self.cache.set(key, financial_report, expire=self.cache_expiry)
            logging.info(f"Scraped and cached financial report for {company.code}, year {year}.")
            return financial_report
        except Exception as e:
            logging.error(f"Error scraping financial report for {company.code}, year {year}: {e}")
            raise

    async def get_announcements(
        self,
        company: Company = None,
        fromdate: datetime.date = datetime.today().date() - timedelta(days=30),
        todate: datetime.date = datetime.today().date(),
        disclosure_type: Optional[List[AnnouncementType]] = None,
        fund_types: List[FundType] = FundType.default(),
        member_types: List[MemberType] = MemberType.default(),
    ) -> List[Disclosure]:
        oid = None
        if company:
            try:
                oid = _search_oid(company)
                logging.info(f"Retrieved OID for company {company.code}.")
            except Exception as e:
                logging.error(f"Error retrieving OID for company {company.code}: {e}")
                raise

        data = {
            "fromDate": fromdate.strftime("%d.%m.%Y"),
            "toDate": todate.strftime("%d.%m.%Y"),
            "disclosureType": disclosure_type,
            "fundTypes": fund_types,
            "memberTypes": member_types,
            "mkkMemberOid": oid,
        }
        try:
            response = requests.post("https://www.kap.org.tr/tr/api/disclosure/list/main", json=data)
            response.raise_for_status()
            json_data = response.json()
            disclosures = [
                Disclosure(
                    disclosureBasic=DisclosureBasic(**item["disclosureBasic"]),
                    disclosureDetail=DisclosureDetail(**item["disclosureDetail"])
                ) for item in json_data
            ]
            logging.info(f"Retrieved {len(disclosures)} announcements.")
            return disclosures
        except Exception as e:
            logging.error(f"Error retrieving announcements: {e}")
            raise

    async def get_sectors(self, fetch_remote: bool = False) -> List[Sector]:
        key = "sectors"
        if not fetch_remote:
            cached_sectors = self.cache.get(key=key)
            if cached_sectors:
                logging.info("Returning cached sectors list.")
                return [Sector(**sector) for sector in cached_sectors]
        try:
            sectors = await scrape_sectors()
            self.cache.set(key, [sector.dict() for sector in sectors], expire=self.sectors_cache_expiry)
            logging.info(f"Scraped and cached {len(sectors)} sectors.")
            return sectors
        except Exception as e:
            logging.error(f"Error scraping sectors: {e}")
            raise

    def clear_cache(self) -> None:
        self.cache.clear()
        logging.info("Cache cleared.")
