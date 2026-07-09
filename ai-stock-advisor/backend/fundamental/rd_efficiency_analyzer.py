class RDEfficiencyAnalyzer:
    """
    Evaluates R&D efficiency using
    R&D spending relative to revenue.
    """

    @staticmethod
    def _safe(value):
        return 0 if value is None else value

    def analyze(
        self,
        mapped,
    ):

        revenue = self._safe(
            mapped.get("revenue")
        )

        research = self._safe(
            mapped.get("research_and_development")
        )

        rd_ratio = 0

        if revenue > 0:
            rd_ratio = (
                research
                / revenue
            ) * 100

        score = 1

        if rd_ratio >= 15:
            score = 5

        elif rd_ratio >= 10:
            score = 4

        elif rd_ratio >= 5:
            score = 3

        elif rd_ratio >= 2:
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
            "rd_ratio": rd_ratio,
            "quality": quality,
        }