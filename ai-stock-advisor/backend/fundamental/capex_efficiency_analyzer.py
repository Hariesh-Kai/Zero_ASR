class CapexEfficiencyAnalyzer:
    """
    Measures how efficiently capital expenditure
    generates revenue.
    """

    @staticmethod
    def _safe(value):
        return 0 if value is None else value

    def analyze(self, mapped):

        revenue = self._safe(
            mapped.get("revenue")
        )

        capital_expenditure = abs(
            self._safe(
                mapped.get("capital_expenditure")
            )
        )

        efficiency = 0

        if capital_expenditure > 0:
            efficiency = (
                revenue
                / capital_expenditure
            )

        score = 1

        if efficiency >= 6:
            score = 5

        elif efficiency >= 5:
            score = 4

        elif efficiency >= 4:
            score = 3

        elif efficiency >= 3:
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
            "capex_efficiency": efficiency,
            "quality": quality,
        }