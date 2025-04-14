from dataclasses import dataclass
from typing import Optional, List

@dataclass
class DisclosureBasic:
    title: str
    mkkMemberOid: str
    companyTitle: str
    stockCode: Optional[str]
    relatedStocks: Optional[str]
    disclosureClass: str
    disclosureType: str
    disclosureCategory: str
    publishDate: str
    disclosureId: str
    disclosureIndex: int
    summary: str
    attachmentCount: int
    year: Optional[int]
    donem: Optional[str]
    period: str
    hasMultiLanguageSupport: str
    fundType: Optional[str]
    isLate: bool
    relatedDisclosureOid: Optional[str]
    senderType: Optional[str]
    isChanged: Optional[bool]
    isBlocked: bool

@dataclass
class DisclosureDetail:
    ftNiteligi: Optional[str]
    decimalDegree: Optional[float]
    opinion: Optional[str]
    opinionType: Optional[str]
    auditType: Optional[str]
    mainDisclosureDocumentId: str
    opinionMemberTitle: Optional[str]
    relatedDisclosureIndex: Optional[int]
    oldKap: bool
    fundOid: Optional[str]
    senderTypes: Optional[str]
    nonInactiveCount: Optional[int]
    blockedDescription: Optional[str]
    memberType: Optional[str]

@dataclass
class Disclosure:
    disclosureBasic: DisclosureBasic
    disclosureDetail: DisclosureDetail
