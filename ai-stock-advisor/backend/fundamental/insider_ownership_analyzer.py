class InsiderOwnershipAnalyzer:
    """
    Evaluates insider ownership as a measure
    of management alignment with shareholders.
    """

    @staticmethod
    def _safe(value):
        return 0 if value is None else value

    def analyze(
        self,
        company_info,
    ):

        insider_percent = self._safe(
            company_info.get("heldPercentInsiders")
        )

        insider_percent *= 100

        score = 1

        if insider_percent >= 20:
            score = 5

        elif insider_percent >= 10:
            score = 4

        elif insider_percent >= 5:
            score = 3

        elif insider_percent >= 1:
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
            quality = "Low"

        else:
            quality = "Very Low"

        return {
            "score": score,
            "max_score": 5,
            "insider_ownership": insider_percent,
            "quality": quality,
        }