class CROICAnalyzer:
    """
    Calculates Cash Return on Invested Capital (CROIC).
    """

    @staticmethod
    def _safe(value):
        return 0 if value is None else value

    def analyze(
        self,
        mapped,
    ):

        operating_cash_flow = self._safe(
            mapped.get("operating_cash_flow")
        )

        total_debt = self._safe(
            mapped.get("total_debt")
        )

        shareholder_equity = self._safe(
            mapped.get("shareholder_equity")
        )

        invested_capital = (
            total_debt +
            shareholder_equity
        )

        croic = 0

        if invested_capital > 0:
            croic = (
                operating_cash_flow
                / invested_capital
            ) * 100

        score = 1

        if croic >= 25:
            score = 5

        elif croic >= 20:
            score = 4

        elif croic >= 15:
            score = 3

        elif croic >= 10:
            score = 2

        else:
            score = 1

        if score == 5:
            quality = "Excellent"

        elif score == 4:
            quality = "Good"

        elif score == 3:
            quality = "Average"

        elif score == 2:
            quality = "Weak"

        else:
            quality = "Poor"

        return {
            "score": score,
            "max_score": 5,
            "croic": croic,
            "invested_capital": invested_capital,
            "quality": quality,
        }