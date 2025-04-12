from dataclasses import dataclass


@dataclass
class CompanyInfo:
    address: str = ""
    mail: list[str] = None
    website: str = ""
    companys_duration: str = ""
    independent_audit_firm: str = ""
    indices: list[str] = None
    sectors: list[str] = None
    equity_market: str = ""
