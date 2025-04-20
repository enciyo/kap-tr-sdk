from asyncio.log import logger
from pyppeteer import launch
from bs4 import BeautifulSoup
from kap_sdk.models.company import Company
from kap_sdk.models.company import Company
from kap_sdk.models.company_info import CompanyInfo

_GENERAL_URL = "https://www.kap.org.tr/tr/sirket-bilgileri/ozet/"

def _find_cells(
    soup: BeautifulSoup,
    string: str,
) -> list[str]:
    data = soup.find('h3', string=string)
    if data:
        next_container = data.find_next(["p", "div"])
        if next_container is None:
            return [""]
        text_elements = next_container.find_all(string=True, recursive=True)
        if not text_elements:
            return [""]
        return [a.text for a in text_elements]
    return [""]


async def scrape_company_info(company: Company) -> CompanyInfo:
    browser = None
    try:
        browser = await launch(
            handleSIGINT = "false",
            handleSIGTERM = "false",
            handleSIGHUP = "false",
        )
        page = await browser.newPage()
        await page.goto(_GENERAL_URL + company.path, {"waitUntil": "domcontentloaded"})
        await page.waitForSelector('#financialTable', timeout=10000)
        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')
        info = CompanyInfo()


        info.address = _find_cells(soup, 'Merkez Adresi')[0]
        info.mail = _find_cells(soup, 'Elektronik Posta Adresi')
        info.website = _find_cells(soup, 'İnternet Adresi')[0]
        info.companys_duration = _find_cells(soup, 'Şirketin Süresi')[0]
        info.independent_audit_firm = _find_cells(soup, 'Bağımsız Denetim Kuruluşu')[0]
        info.indices = _find_cells(soup, 'Şirketin Dahil Olduğu Endeksler')
        info.sectors = _find_cells(soup, 'Şirketin Sektörü')
        info.equity_market = _find_cells(soup, 'Sermaye Piyasası Aracının İşlem Gördüğü Pazar')[0]
        return info
    except Exception as e:
        logger.error(f"Error scraping company info: {e}")
        return None
    finally:
        if browser:
            await browser.close()



