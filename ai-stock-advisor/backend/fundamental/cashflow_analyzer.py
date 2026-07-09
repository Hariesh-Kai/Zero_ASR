from fundamental.ratios.cashflow import CashFlowRatios


class CashFlowAnalyzer:
    """
    Performs cash flow analysis using standardized financial data.
    """

    def __init__(self):
        self.ratios = CashFlowRatios()

    def analyze(
        self,
        mapped,
        growth,
    ):

        operating_cash_flow = mapped.get("operating_cash_flow")
        capital_expenditure = mapped.get("capital_expenditure")

        current_liabilities = mapped.get("current_liabilities")

        net_income = mapped.get("net_income")

        free_cash_flow = self.ratios.free_cash_flow(
            operating_cash_flow,
            capital_expenditure,
        )

        operating_cash_flow_ratio = self.ratios.operating_cash_flow_ratio(
            operating_cash_flow,
            current_liabilities,
        )

        cash_conversion_ratio = self.ratios.cash_conversion_ratio(
            operating_cash_flow,
            net_income,
        )

        return {
            "operating_cash_flow": operating_cash_flow,
            "free_cash_flow": free_cash_flow,
            "cashflow_growth": growth.get("cashflow_growth"),
            "operating_cash_flow_ratio": operating_cash_flow_ratio,
            "cash_conversion_ratio": cash_conversion_ratio,
        }