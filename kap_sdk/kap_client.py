import diskcache
from _companies import scrape_companies
from _indices import scrape_indices
from _company_info import scrape_company_info
from _financial_report import get_financial_report
from models.company import Company
from models.indices import Indice
from models.company_info import CompanyInfo
from typing import Optional

_CACHE_KEY = "kap_cache"

class KapClient:

    def __init__(
        self,
        cache_expiry=3600
    ):
        self.cache = diskcache.Cache(_CACHE_KEY)
        self.cache_expiry = cache_expiry

    async def get_companies(self) -> list[Company]:
        key = "companies"
        cached_companies = self.cache.get(key=key)
        if cached_companies:
            return cached_companies
        companies = await scrape_companies()
        self.cache.set(key, companies, expire=self.cache_expiry)
        return companies

    async def get_indices(self) -> list[Indice]:
        key = "indices"
        cached_indices = self.cache.get(key=key)
        if cached_indices:
            return cached_indices
        indices = await scrape_indices()
        self.cache.set(key, indices, expire=self.cache_expiry)
        return indices

    async def get_company(self, code: str) -> Optional[Company]:
        companies = await self.get_companies()
        for company in companies:
            if company.code == code:
                return company
        return None

    async def get_indice(self, code: str) -> Optional[Indice]:
        indices = await self.get_indices()
        for indice in indices:
            if indice.code == code:
                return indice
        return None

    async def get_company_info(self, company: Company) -> Optional[CompanyInfo]:
        key = f"infos_{company.code}"
        cached_company_info = self.cache.get(key=key)
        if cached_company_info:
            return cached_company_info
        company_info = await scrape_company_info(company)
        self.cache.set(key, company_info, expire=self.cache_expiry)
        return company_info

    async def get_financial_report(self, company: Company, year: str = "2023") -> dict:
        key = f"financial_report_{company.code}_{year}"
        cached_financial_report = self.cache.get(key=key)
        if cached_financial_report:
            return cached_financial_report
        financial_report = await get_financial_report(company=company, year=year)
        self.cache.set(key, financial_report, expire=self.cache_expiry)
        return financial_report


    def clear_cache(self):
        self.cache.clear()


