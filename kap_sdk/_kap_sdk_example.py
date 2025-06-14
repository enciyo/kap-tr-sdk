import asyncio

from kap_sdk.kap_client import KapClient
import json
import os


SAMPLE_DIR = "samples"
if not os.path.exists(SAMPLE_DIR):
    os.makedirs(SAMPLE_DIR)


def save_sample_md(name, data):
    filename = os.path.join(SAMPLE_DIR, f"{name}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    


async def sample_get_company():
    client = KapClient()
    company = await client.get_company("BIMAS")
    save_sample_md("BIMAS", company.dict())


async def sample_get_company_info():
    client = KapClient()
    company = await client.get_company("BIMAS")
    info = await client.get_company_info(company)
    save_sample_md("BIMAS", info.dict())


async def sample_get_financial_report():
    client = KapClient()
    company = await client.get_company("BIMAS")
    report = await client.get_financial_report(company, "2023")
    save_sample_md("BIMAS", report)


async def sample_get_indices():
    client = KapClient()
    indices = await client.get_indices()
    if not indices:
        print("No indices found.")
        return
    # Indice nesnelerini JSON seri hale getirmek için dict() metodunu kullanıyoruz
    indices_dict = [indice.dict() for indice in indices]
    save_sample_md("indices", indices_dict)


async def sample_get_announcements_by_company():
    client = KapClient()
    company = await client.get_company("BIMAS")
    announce = await client.get_announcements(company)
    # Disclosure nesnelerini JSON seri hale getirmek için dict() metodunu kullanıyoruz
    announce_dict = [{"disclosureBasic": item.disclosureBasic.dict(), "disclosureDetail": item.disclosureDetail.dict()} for item in announce]
    save_sample_md("announcements_by_company", announce_dict)


async def sample_get_announcements():
    client = KapClient()
    announcements = await client.get_announcements()
    # Disclosure nesnelerini JSON seri hale getirmek için dict() metodunu kullanıyoruz
    announcements_dict = [{"disclosureBasic": item.disclosureBasic.dict(), "disclosureDetail": item.disclosureDetail.dict()} for item in announcements]
    save_sample_md("announcements", announcements_dict)


async def sample_get_sectors():
    client = KapClient()
    sectors = await client.get_sectors()
    # Sector nesnelerini JSON seri hale getirmek için dict() metodunu kullanıyoruz
    sectors_dict = [sector.dict() for sector in sectors]
    save_sample_md("sectors", sectors_dict)


async def main():
    await sample_get_company()
    await sample_get_company_info()
    await sample_get_indices()
    await sample_get_announcements_by_company()
    await sample_get_announcements()
    await sample_get_sectors()
    await sample_get_financial_report()

if __name__ == "__main__":
    asyncio.run(main=main())
