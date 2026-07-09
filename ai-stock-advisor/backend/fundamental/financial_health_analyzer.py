from fundamental.ratios.financial_health import FinancialHealthRatios


class FinancialHealthAnalyzer:
    """
    Performs financial health analysis.
    """

    def __init__(self):
        self.ratios = FinancialHealthRatios()

    def analyze(self, mapped):

        ebit = mapped.get("ebit")
        ebitda = mapped.get("ebitda")
        interest_expense = mapped.get("interest_expense")

        total_debt = mapped.get("total_debt")
        total_assets = mapped.get("total_assets")
        shareholder_equity = mapped.get("shareholder_equity")

        return {
            "interest_coverage": self.ratios.interest_coverage(
                ebit,
                interest_expense,
            ),
            "debt_to_ebitda": self.ratios.debt_to_ebitda(
                total_debt,
                ebitda,
            ),
            "financial_leverage": self.ratios.financial_leverage(
                total_assets,
                shareholder_equity,
            ),
        }