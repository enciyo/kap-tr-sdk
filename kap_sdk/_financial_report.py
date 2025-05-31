import requests
from bs4 import BeautifulSoup
from kap_sdk._search_oid import _search_oid
from kap_sdk.models.company import Company
import zipfile
import io
import pandas as pd
from io import StringIO
from typing import List, Dict, Union
import pandas as pd

DOWNLOAD_URL = "https://www.kap.org.tr/tr/api/home-financial/download-file/"


def _download_xls(mkkMemberOid: str, year: str) -> str:
    # Burada dosyayı indiriyor
    data = requests.get(f"{DOWNLOAD_URL}{mkkMemberOid}/{year}/T", stream=False)
    data.raise_for_status()
    return data.content



def _extract_data(path: str, price: float, table_indices: List[int] = [1, 300, 453]) -> List[Dict[str, Union[str, float]]]:
    tables = pd.read_html(path)
    selected_tables = [tables[i].iloc[:, [1, 3]].dropna().reset_index(drop=True) for i in table_indices if i < len(tables)]

    concat_table = pd.concat(selected_tables, ignore_index=True)
    concat_table.columns = ['key', 'value']

    def clean_value(value: str, price: float) -> Union[float, None]:
        try:
            cleaned_value = value.strip().replace(".", "").replace(",", ".")
            return float(cleaned_value) * price
        except ValueError:
            print(f"Could not convert value: {value}")
            return None

    concat_table['value'] = concat_table['value'].apply(lambda x: clean_value(x, price))
    concat_table.dropna(inplace=True)

    extracted_data = []
    for index, row in concat_table.iterrows():
        extracted_data.append({
            "key": row['key'].strip(),
            "value": row['value']
        })

    return extracted_data




def _find_financial_header_title(data: str) -> dict:
    soup = BeautifulSoup(data, 'html.parser')
    header = soup.find('table', {'class': 'financial-header-table'})
    row_title = header.find_all('tr')[1].find_all(
        "td")[1].text.strip().lower().replace(" ", "_")
    row_price = header.find_all('tr')[0].find_all(
        "td")[1].text.strip().replace("TL", "").replace(".", "")

    try:
        price = float(row_price)
    except ValueError:
        price = 1.0

    return {
        "title": row_title,
        "price": price
    }


async def get_financial_report(company: Company, year: str = "2023") -> dict:
    oid = _search_oid(company)
    content = _download_xls(oid, year=year)
    try:
        zip_file = io.BytesIO(content)
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
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
                        StringIO(data.decode('utf-8')), meta['price'])
    except Exception as e:
        print(f"Error extracting financial report: {e}")
        raise e
    finally:
        pass

    return extracted_data
