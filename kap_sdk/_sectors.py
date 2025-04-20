import logging
from bs4 import BeautifulSoup
from pyppeteer import launch
from kap_sdk.models.sectors import Sector, SubSector

_URL ="https://www.kap.org.tr/tr/Sektorler"

async def scrape_sectors() -> list[Sector]:
    sectors = []
    browser = None

    try:
        browser = await launch(
            handleSIGINT = "false",
            handleSIGTERM = "false",
            handleSIGHUP = "false",
        )
        page = await browser.newPage()

        await page.goto(_URL, {"waitUntil": "domcontentloaded"})
        await page.waitForSelector('#sectorsTable', timeout=10000)
        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')
        table = soup.find(id='sectorsTable')

        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            if len(cols) == 1:
                spans = cols[0].find_all('span')
                sector_name = spans[0].text.strip() if spans else None
                if sector_name:
                    sector = Sector(name=sector_name, sub_sectors=[],companies=[])
                    sectors.append(sector)
                else:
                    sub_sector_name = cols[0].text.strip()
                    if "Kayıt Bulunmadı" in sub_sector_name:
                        continue

                    sub_sector = SubSector(
                        name=sub_sector_name,
                        companies=[]
                    )
                    last_sector : Sector = sectors[-1]
                    if last_sector:
                        last_sector.sub_sectors.append(sub_sector)

            elif len(cols) == 4:
                code = cols[1].text.strip()
                last_sector: Sector = sectors[-1]
                if len(last_sector.sub_sectors) > 0:
                    last_sub_sector: SubSector = last_sector.sub_sectors[-1]
                    last_sub_sector.companies.append(code)
                else:
                    last_sector.companies.append(code)

    except Exception as e:
        logging.error(f"Scraping failed: {e}")
        raise e
    finally:
        if browser:
            await browser.close()
    return sectors


