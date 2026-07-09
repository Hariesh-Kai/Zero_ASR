class FCFYieldAnalyzer:
    """
    Evaluates valuation using
    Free Cash Flow Yield.
    """

    @staticmethod
    def _safe(value):
        return 0 if value is None else value

    def analyze(
        self,
        mapped,
    ):

        free_cash_flow = self._safe(
            mapped.get("free_cash_flow")
        )

        market_cap = self._safe(
            mapped.get("market_cap")
        )

        fcf_yield = 0

        if market_cap > 0:
            fcf_yield = (
                free_cash_flow
                / market_cap
            ) * 100

        if fcf_yield >= 8:
            score = 5
            valuation = "Deeply Undervalued"

        elif fcf_yield >= 6:
            score = 4
            valuation = "Undervalued"

        elif fcf_yield >= 4:
            score = 3
            valuation = "Fair"

        elif fcf_yield >= 2:
            score = 2
            valuation = "Expensive"

        else:
            score = 1
            valuation = "Very Expensive"

        return {
            "score": score,
            "max_score": 5,
            "fcf_yield": fcf_yield,
            "valuation": valuation,
        }