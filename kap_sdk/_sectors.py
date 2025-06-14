import logging
from bs4 import BeautifulSoup
from pyppeteer import launch
from kap_sdk.models.sectors import Sector, SubSector

# KAP sektörler sayfasının URL'si
_URL = "https://www.kap.org.tr/tr/Sektorler"

async def scrape_sectors() -> list[Sector]:
    """
    KAP websitesinden sektör ve alt sektör bilgilerini kazır.
    Returns:
        list[Sector]: Sektör ve alt sektör bilgilerini içeren liste.
    """
    sectors: list[Sector] = []
    browser = None

    try:
        # Tarayıcıyı başlat ve sinyal yönetimini devre dışı bırak
        browser = await launch(
            handleSIGINT="false",
            handleSIGTERM="false",
            handleSIGHUP="false",
        )
        page = await browser.newPage()

        # Belirtilen URL'ye git ve DOM'un yüklenmesini bekle
        await page.goto(_URL, {"waitUntil": "domcontentloaded"})
        await page.waitForSelector('#sectorsTable', timeout=10000)
        
        # Sayfa içeriğini al ve BeautifulSoup ile ayrıştır
        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')
        table = soup.find(id='sectorsTable')

        # Tablo satırlarını döngüye al, başlık satırını atla
        for row in table.find_all('tr')[1:]:
            columns = row.find_all('td')
            if len(columns) == 1:
                # Sektör veya alt sektör adı kontrolü
                spans = columns[0].find_all('span')
                sector_name = spans[0].text.strip() if spans else None
                if sector_name:
                    # Yeni bir sektör oluştur ve listeye ekle
                    sector = Sector(name=sector_name, sub_sectors=[], companies=[])
                    sectors.append(sector)
                else:
                    sub_sector_name = columns[0].text.strip()
                    if "Kayıt Bulunmadı" in sub_sector_name:
                        continue

                    # Yeni bir alt sektör oluştur ve son sektöre ekle
                    sub_sector = SubSector(
                        name=sub_sector_name,
                        companies=[]
                    )
                    last_sector: Sector = sectors[-1]
                    if last_sector:
                        last_sector.sub_sectors.append(sub_sector)

            elif len(columns) == 4:
                # Şirket kodu ekle
                company_code = columns[1].text.strip()
                last_sector: Sector = sectors[-1]
                if len(last_sector.sub_sectors) > 0:
                    last_sub_sector: SubSector = last_sector.sub_sectors[-1]
                    last_sub_sector.companies.append(company_code)
                else:
                    last_sector.companies.append(company_code)

    except Exception as e:
        logging.error(f"Sektör kazıma işlemi başarısız oldu: {e}")
        raise e
    finally:
        # Tarayıcıyı kapat
        if browser:
            await browser.close()
    return sectors
