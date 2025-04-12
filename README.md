# kap_sdk

A Python SDK for scraping data from KAP (Public Disclosure Platform).

## Installation

```bash
pip install kap_sdk
```

## Dependencies

*   requests
*   beautifulsoup4
*   pyppeteer

## Usage

```python
from kap_sdk.kap_client import KapClient
import asyncio

async def main():
    client = KapClient()

    companies = await client.get_companies()
    print(f"Found {len(companies)} companies.")

    indices = await client.get_indices()
    print(f"Found {len(indices)} indices.")

    if companies:
        company = await client.get_company(companies[0].code)
        print(f"Company info: {company}")

        company_info = await client.get_company_info(company)
        print(f"Company details: {company_info}")

        financial_report = await client.get_financial_report(company)
        print(f"Financial report: {financial_report}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Future Features

*   Company announcements retrieval
