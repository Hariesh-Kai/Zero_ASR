class EPSConsistencyAnalyzer:
    """
    Measures the consistency of Earnings Per Share (EPS)
    growth between reporting periods.
    """

    @staticmethod
    def _safe(value):
        return 0 if value is None else value

    def analyze(
        self,
        mapped,
        previous_mapped,
    ):

        current_eps = self._safe(
            mapped.get("eps")
        )

        previous_eps = self._safe(
            previous_mapped.get("eps")
        )

        growth = 0

        if previous_eps > 0:
            growth = (
                (current_eps - previous_eps)
                / previous_eps
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
            "eps_growth": growth,
            "quality": quality,
        }