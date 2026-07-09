class EarningsStabilityAnalyzer:
    """
    Measures the stability of earnings growth
    between reporting periods.
    """

    @staticmethod
    def _safe(value):
        return 0 if value is None else value

    def analyze(
        self,
        mapped,
        previous_mapped,
    ):

        current_earnings = self._safe(
            mapped.get("net_income")
        )

        previous_earnings = self._safe(
            previous_mapped.get("net_income")
        )

        growth = 0

        if previous_earnings > 0:
            growth = (
                (current_earnings - previous_earnings)
                / previous_earnings
            ) * 100

        score = 1

        if 5 <= growth <= 20:
            score = 5

        elif 0 <= growth < 5:
            score = 4

        elif 20 < growth <= 35:
            score = 4

        elif -5 <= growth < 0:
            score = 3

        elif growth > 35:
            score = 2

        if score == 5:
            quality = "Excellent"

        elif score == 4:
            quality = "Good"

        elif score == 3:
            quality = "Average"

        elif score == 2:
            quality = "Volatile"

        else:
            quality = "Poor"

        return {
            "score": score,
            "max_score": 5,
            "earnings_growth": growth,
            "quality": quality,
        }