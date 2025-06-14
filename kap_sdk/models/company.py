from dataclasses import asdict, dataclass
import logging
from pyppeteer import launch
from bs4 import BeautifulSoup
from typing import List
from kap_sdk import _get_browser_config

@dataclass
class Company:
    path: str = ""
    name: str = ""
    code: str = ""
    city: str = ""
    independent_audit_firm: str = ""

    def dict(self):
        return asdict(self)

URL = "https://www.kap.org.tr/tr/bist-sirketler"

def _parse_row(row):
    """Parse a table row to extract company information.
    
    Args:
        row: A BeautifulSoup row element from the companies table.
        
    Returns:
        Company: A Company object with parsed data, or None if parsing fails.
    """
    cols = row.find_all('td')
    if len(cols) < 4:
        return None
    return Company(
        code=cols[0].text.strip(),
        name=cols[1].text.strip(),
        city=cols[2].text.strip(),
        independent_audit_firm=cols[3].text.strip(),
        path=cols[1].find('a')['href'].strip().split('/')[-1]
    )

async def scrape_companies() -> List[Company]:
    """Scrape company data from KAP website.
    
    Returns:
        List[Company]: A list of Company objects with data from the KAP website.
    """
    companies = []
    browser = None

    try:
        config = _get_browser_config()
        browser = await launch(**config)
        page = await browser.newPage()

        await page.goto(URL, {"waitUntil": "domcontentloaded"})
        await page.waitForSelector('#financialTable', timeout=10000)
        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')
        table = soup.find(id='financialTable')

        for row in table.find_all('tr')[1:]:
            company = _parse_row(row)
            if company:
                companies.append(company)
    except Exception as e:
        logging.error(f"Scraping failed: {e}")
    finally:
        if browser:
            await browser.close()

    return companies
