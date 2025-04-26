import requests
from bs4 import BeautifulSoup
from kap_sdk._search_oid import _search_oid
from kap_sdk.models.company import Company
import zipfile
import os
import shutil


DOWNLOAD_URL = "https://www.kap.org.tr/tr/api/home-financial/download-file/"


def _download_xls(mkkMemberOid: str, year: str) -> str:
    # Burada dosyayı indiriyor
    data = requests.get(f"{DOWNLOAD_URL}{mkkMemberOid}/{year}/T", stream=False)
    data.raise_for_status()
    return data.content


def _extract_data(data: str) -> dict:
    soup = BeautifulSoup(data, 'html.parser')
    table = soup.find(
        'table', {'class': 'financial-table'})
    extracted_data = []
    rows = table.find_all('tr')[7:]
    for row in rows:
        cells = row.find_all('td')
        if cells:
            key_cell = cells[1].find(
                'div', {'class': 'gwt-Label'}) if len(cells) > 1 else None
            value_cell = cells[7] if len(cells) > 7 else None

            key = key_cell.text.strip() if key_cell else ""
            value = value_cell.text.strip() if value_cell else ""

            if key or value:
                extracted_data.append({"key": key, "value": value})

    return extracted_data


def _find_financial_header_title(soup: BeautifulSoup) -> dict:
    soup = BeautifulSoup(soup, 'html.parser')
    header = soup.find('table', {'class': 'financial-header-table'})
    row_title = header.find_all('tr')[1].find_all("td")[1].text.strip().lower().replace(" ", "_")

    return {
        "title": row_title,
    }


async def get_financial_report(company: Company, year: str = "2023") -> dict:
    oid = _search_oid(company)
    content = _download_xls(oid, year=year)
    zip_file_path = f"{company.code}_financial_report.zip"
    try:
        with open(zip_file_path, "wb") as file:
            file.write(content)

        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(f"{company.code}_financial_report")
            files = zip_ref.namelist()
            if len(files) == 0:
                raise ValueError(
                    f"No found {company.code} financial report for {year}")
            extracted_data = {}
            for file_name in zip_ref.namelist():
                if file_name.endswith('.xls'):
                    with zip_ref.open(file_name) as file:
                        data = file.read()
                        meta = _find_financial_header_title(data)
                        period = f"period_{file_name.split('_')[-1]}_{meta['title']}"
                        period = period.replace('.xls', '')
                        extracted_data[period] = _extract_data(
                            data)
    except Exception as e:
        print(f"Error extracting financial report: {e}")
        raise e
    finally:
        pass
        if os.path.exists(zip_file_path):
            os.remove(zip_file_path)
        if os.path.exists(f"{company.code}_financial_report"):
            shutil.rmtree(f"{company.code}_financial_report")

    return extracted_data
