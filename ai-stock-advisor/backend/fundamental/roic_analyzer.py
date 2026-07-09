class ROICAnalyzer:
    """
    Measures how efficiently a company generates returns
    from the capital invested in the business.

    ROIC = NOPAT / Invested Capital
    """

    @staticmethod
    def _safe(value):
        return 0 if value is None else value

    def analyze(self, mapped):

        ebit = self._safe(
            mapped.get("ebit")
        )

        total_debt = self._safe(
            mapped.get("total_debt")
        )

        shareholder_equity = self._safe(
            mapped.get("shareholder_equity")
        )

        cash = self._safe(
            mapped.get("cash")
        )

        # Assume 21% corporate tax
        tax_rate = 0.21

        nopat = ebit * (1 - tax_rate)

        invested_capital = (
            total_debt
            + shareholder_equity
            - cash
        )

        roic = 0

        if invested_capital > 0:
            roic = (
                nopat
                / invested_capital
            ) * 100

        score = 1

        if roic >= 20:
            score = 5

        elif roic >= 15:
            score = 4

        elif roic >= 10:
            score = 3

        elif roic >= 5:
            score = 2

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
            "roic": roic,
            "nopat": nopat,
            "invested_capital": invested_capital,
            "quality": quality,
        }