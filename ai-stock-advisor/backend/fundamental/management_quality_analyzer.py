class ManagementQualityAnalyzer:
    """
    Evaluates management quality using
    profitability and capital allocation metrics.
    """

    @staticmethod
    def _safe(value):
        return 0 if value is None else value

    def analyze(
        self,
        mapped,
    ):

        roe = self._safe(
            mapped.get("net_income")
        )

        equity = self._safe(
            mapped.get("shareholder_equity")
        )

        roe_percent = 0

        if equity > 0:
            roe_percent = (
                roe / equity
            ) * 100

        score = 1

        if roe_percent >= 20:
            score = 5

        elif roe_percent >= 15:
            score = 4

        elif roe_percent >= 10:
            score = 3

        elif roe_percent >= 5:
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
            "roe": roe_percent,
            "quality": quality,
        }