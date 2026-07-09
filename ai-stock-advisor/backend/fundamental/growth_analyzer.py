from fundamental.ratios.growth import GrowthRatios


class GrowthAnalyzer:
    """
    Performs company growth analysis using historical financial statements.
    """

    def __init__(self):
        self.ratios = GrowthRatios()

    def analyze(self, income_statement, cash_flow):

        income_years = list(income_statement.values())
        cash_years = list(cash_flow.values())

        if len(income_years) < 2:
            return {}

        current_income = income_years[0]
        previous_income = income_years[1]

        current_cash = cash_years[0] if len(cash_years) > 0 else {}
        previous_cash = cash_years[1] if len(cash_years) > 1 else {}

        # Revenue Growth
        revenue_growth = self.ratios.revenue_growth(
            current_income.get("Total Revenue"),
            previous_income.get("Total Revenue"),
        )

        # Earnings Growth
        earnings_growth = self.ratios.earnings_growth(
            current_income.get("Net Income"),
            previous_income.get("Net Income"),
        )

        eps_growth = self.ratios.eps_growth(
            current_income.get("Diluted EPS"),
            previous_income.get("Diluted EPS"),
        )

        # Cash Flow Growth
        cashflow_growth = self.ratios.cashflow_growth(
            current_cash.get("Operating Cash Flow"),
            previous_cash.get("Operating Cash Flow"),
        )

        return {
            "revenue_growth": revenue_growth,
            "earnings_growth": earnings_growth,
            "eps_growth": eps_growth,
            "cashflow_growth": cashflow_growth,
        }