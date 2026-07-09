class WorkingCapitalQualityAnalyzer:
    """
    Evaluates the quality of a company's
    working capital position.
    """

    @staticmethod
    def _safe(value):
        return 0 if value is None else value

    def analyze(
        self,
        mapped,
    ):

        current_assets = self._safe(
            mapped.get("current_assets")
        )

        current_liabilities = self._safe(
            mapped.get("current_liabilities")
        )

        working_capital = (
            current_assets
            - current_liabilities
        )

        ratio = 0

        if current_liabilities > 0:
            ratio = (
                current_assets
                / current_liabilities
            )

        score = 1

        if ratio >= 2:
            score = 5

        elif ratio >= 1.5:
            score = 4

        elif ratio >= 1.2:
            score = 3

        elif ratio >= 1:
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
            "working_capital": working_capital,
            "working_capital_ratio": ratio,
            "quality": quality,
        }