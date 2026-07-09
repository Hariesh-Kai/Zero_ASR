class ShareDilutionAnalyzer:
    """
    Measures whether the company is reducing
    or increasing its shares outstanding.
    """

    @staticmethod
    def _safe(value):
        return 0 if value is None else value

    def analyze(
        self,
        mapped,
        previous_mapped,
    ):

        current_shares = self._safe(
            mapped.get("shares_outstanding")
        )

        previous_shares = self._safe(
            previous_mapped.get("shares_outstanding")
        )

        dilution = 0

        if previous_shares > 0:
            dilution = (
                (current_shares - previous_shares)
                / previous_shares
            ) * 100

        score = 1

        # Negative dilution = buybacks
        if dilution <= -5:
            score = 5

        elif dilution <= -2:
            score = 4

        elif dilution <= 0:
            score = 3

        elif dilution <= 2:
            score = 2

        else:
            score = 1

        if score == 5:
            quality = "Excellent"

        elif score == 4:
            quality = "Good"

        elif score == 3:
            quality = "Stable"

        elif score == 2:
            quality = "Slight Dilution"

        else:
            quality = "Heavy Dilution"

        return {
            "score": score,
            "max_score": 5,
            "current_shares": current_shares,
            "previous_shares": previous_shares,
            "dilution_percent": dilution,
            "quality": quality,
        }