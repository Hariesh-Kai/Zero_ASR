class MarginStabilityAnalyzer:
    """
    Measures the consistency of operating margin
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

        current_revenue = self._safe(
            mapped.get("revenue")
        )

        previous_revenue = self._safe(
            previous_mapped.get("revenue")
        )

        current_operating_income = self._safe(
            mapped.get("operating_income")
        )

        previous_operating_income = self._safe(
            previous_mapped.get("operating_income")
        )

        current_margin = 0

        if current_revenue > 0:
            current_margin = (
                current_operating_income
                / current_revenue
            ) * 100

        previous_margin = 0

        if previous_revenue > 0:
            previous_margin = (
                previous_operating_income
                / previous_revenue
            ) * 100

        change = current_margin - previous_margin

        score = 1

        if abs(change) <= 2:
            score = 5

        elif abs(change) <= 5:
            score = 4

        elif abs(change) <= 10:
            score = 3

        elif abs(change) <= 15:
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
            "current_margin": current_margin,
            "previous_margin": previous_margin,
            "margin_change": change,
            "quality": quality,
        }