from kap_sdk.models.company import Company
import requests

URL = "https://www.kap.org.tr/tr/api/member/filter/"

def _search_oid(company: Company) -> dict:
    response = requests.get(f"{URL}{company.code}")
    response.raise_for_status()
    oid = response.json()[0]["mkkMemberOid"]
    if not oid:
        raise Exception(f"Company {company.code} not found.")
    return oid
