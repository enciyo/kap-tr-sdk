import asyncio

from kap_sdk.kap_client import KapClient

async def sample_get_company():
    client = KapClient()
    company = await client.get_company("BIMAS")
    message = f"Sample get company: {company}"
    print(message)

async def sample_get_company_info():
    client = KapClient()
    company = await client.get_company("BIMAS")
    info = await client.get_company_info(company)
    message = f"Sample get company info: {info}"
    print(message)

async def sample_get_financial_report():
    client = KapClient()
    company = await client.get_company("TURSG")
    report = await client.get_financial_report(company, "2025")
    message = f"Sample get financial report: {report}"
    print(message)

async def sample_get_indices():
    client = KapClient()
    indices = await client.get_indices()
    message = f"Sample get indices: {indices}"
    print(message)


async def sample_get_announcements_by_company():
    client = KapClient()
    company = await client.get_company("BIMAS")
    announce = await client.get_announcements(company)
    message = f"Sample get announcements: {announce}"
    print(message)

async def sample_get_announcements():
    client = KapClient()
    announcements = await client.get_announcements()
    message = f"Sample get announcements: {announcements}"
    print(message)


async def sample_get_sectors():
    client = KapClient()
    sectors = await client.get_sectors()
    message = f"Sample get sectors: {sectors}"
    print(message)

async def main():
    await sample_get_company()
    await sample_get_company_info()
    await sample_get_financial_report()
    await sample_get_indices()
    await sample_get_announcements_by_company()
    await sample_get_announcements()


if __name__ == "__main__":
    asyncio.run(main=main())



