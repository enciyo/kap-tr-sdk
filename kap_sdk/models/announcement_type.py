class AnnouncementType:
    MaterialEventDisclosure = "ODA"
    FinancialStatement = "FR"
    RegulatoryAuthorityAnnouncements = "DUY"
    Other = "DG"
    Corporate_Actions = "CA"


class MemberType:
    BistCompanies = "IGS"
    InvestmentFirms = "YK"
    PortfolioManagementCompanies = "PYS"
    RegulatoryAuthorities = "DDK"
    OtherKAPMembers = "DG"

    @staticmethod
    def default():
        return [
            MemberType.BistCompanies,
            MemberType.RegulatoryAuthorities,
        ]


class FundType:
    ETF = "BYF"
    MutualFond = "YF"
    PensionFund = "EYF"
    AutoEnrolmentSystemPensionFund = "OKS"
    ForeignFund = "YYF"
    AssetFinanceFund = "VFF"
    HousingFinanceFund = "KFF"
    RealEstateInvestmentFund = "GMF"
    VentureCapitalInvestmentFund = "GSF"
    ProjectFinanceFund = "PFF"

    @staticmethod
    def default():
        return [
            FundType.ETF,
            FundType.RealEstateInvestmentFund,
            FundType.VentureCapitalInvestmentFund,
            FundType.ProjectFinanceFund,
        ]
