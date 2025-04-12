from dataclasses import dataclass


@dataclass
class Indice:
    name: str = ""
    code: str = ""
    companies: list[str] = None
