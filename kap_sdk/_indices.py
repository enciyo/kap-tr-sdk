import logging
from pyppeteer import launch
from bs4 import BeautifulSoup
from typing import Dict
from kap_sdk.models.indices import Indice


URL = "https://www.kap.org.tr/tr/Endeksler"


async def scrape_indices() -> list[Indice]:
    indices = []
    browser = None

    try:
        browser = await launch(
            handleSIGINT = "false",
            handleSIGTERM = "false",
            handleSIGHUP = "false",
        )
        page = await browser.newPage()
        await page.goto(URL, {"waitUntil": "domcontentloaded"})
        await page.waitForSelector('#indicesTable', timeout=10000)
        await page.evaluate("document.querySelector('#stickyDropdown > div > div').click()")
        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')
        table = soup.find(id='indicesTable')
        indices: Dict[str, Indice] = {}
        last_index: str = ""
        for row in table.find_all('tr')[2:]:
            cols = row.find_all('td')
            if len(cols) == 1:
                spans = cols[0].find_all('span')
                last_index = spans[0].text.strip() if spans else ""
                if last_index and last_index not in indices:
                    indices[last_index] = Indice(last_index)
                    indices[last_index].companies = []
            elif len(cols) == 4:
                if not last_index:
                    logging.error("Last index not set, skipping row")
                    continue
                code = cols[1].text.strip()
                indices[last_index].companies.append(code)

        for value in soup.select('div[class*="select__option"]')[1:]:
            span = value.find_all('span')
            if len(span) < 2:
                continue
            index = span[0].text.strip() if span else ""
            if index not in indices:
                continue
            indices[index].code = span[1].text.strip() if span else ""

    except Exception as e:
        logging.error(f"Scraping failed: {e}")
    finally:
        if browser:
            await browser.close()

    return list(indices.values())
