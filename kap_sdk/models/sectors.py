from dataclasses import dataclass


@dataclass
class Sector:
    name: str = ""
    companies: list[str] = None
    sub_sectors: list['SubSector'] = None



@dataclass
class SubSector:
    name: str = ""
    companies: list[str] = None
