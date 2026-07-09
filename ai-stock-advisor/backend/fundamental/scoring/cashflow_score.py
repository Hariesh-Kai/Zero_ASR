
class CashFlowScore:
    """
    Scores cash flow quality.
    Maximum Score: 100
    """

    @staticmethod
    def score(
        operating_cash_flow,
        free_cash_flow,
        cashflow_growth,
    ):

        score = 0

        # Operating Cash Flow (35)
        if operating_cash_flow is not None and operating_cash_flow > 0:
            score += 35

        # Free Cash Flow (35)
        if free_cash_flow is not None and free_cash_flow > 0:
            score += 35

        # Cash Flow Growth (30)
        if cashflow_growth is not None:
            if cashflow_growth >= 20:
                score += 30
            elif cashflow_growth >= 10:
                score += 20
            elif cashflow_growth >= 5:
                score += 10

        return score