class InstitutionalOwnershipAnalyzer:
    """
    Evaluates institutional ownership as a measure
    of confidence from professional investors.
    """

    @staticmethod
    def _safe(value):
        return 0 if value is None else value

    def analyze(
        self,
        company_info,
    ):

        institutional_percent = self._safe(
            company_info.get("heldPercentInstitutions")
        )

        institutional_percent *= 100

        score = 1

        if institutional_percent >= 80:
            score = 5

        elif institutional_percent >= 60:
            score = 4

        elif institutional_percent >= 40:
            score = 3

        elif institutional_percent >= 20:
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
            "institutional_ownership": institutional_percent,
            "quality": quality,
        }