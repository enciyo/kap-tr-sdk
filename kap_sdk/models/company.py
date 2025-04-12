from dataclasses import dataclass


@dataclass
class Company:
    path: str = ""
    name: str = ""
    code: str = ""
    city: str = ""
    independent_audit_firm: str = ""
