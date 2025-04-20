import logging
from pyppeteer import launch
from bs4 import BeautifulSoup
from kap_sdk.models.company import Company

URL = "https://www.kap.org.tr/tr/bist-sirketler"

def _parse_row(row):
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


async def scrape_companies() -> list[Company]:
    companies = []
    browser = None

    try:
        browser = await launch(
            handleSIGINT = "false",
            handleSIGTERM = "false",
            handleSIGHUP = "false",
        )
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
