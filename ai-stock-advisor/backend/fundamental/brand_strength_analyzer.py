class BrandStrengthAnalyzer:
    """
    Evaluates brand strength using
    profitability and market position.
    """

    @staticmethod
    def _safe(value):
        return 0 if value is None else value

    def analyze(
        self,
        mapped,
    ):

        gross_margin = 0
        operating_margin = 0

        revenue = self._safe(
            mapped.get("revenue")
        )

        gross_profit = self._safe(
            mapped.get("gross_profit")
        )

        operating_income = self._safe(
            mapped.get("operating_income")
        )

        if revenue > 0:

            gross_margin = (
                gross_profit
                / revenue
            ) * 100

            operating_margin = (
                operating_income
                / revenue
            ) * 100

        score = 1

        if gross_margin >= 70:
            score += 2

        elif gross_margin >= 50:
            score += 1

        if operating_margin >= 30:
            score += 2

        elif operating_margin >= 20:
            score += 1

        score = min(score, 5)

        if score == 5:
            quality = "Excellent"

        elif score == 4:
            quality = "Strong"

        elif score == 3:
            quality = "Average"

        elif score == 2:
            quality = "Weak"

        else:
            quality = "Poor"

        return {
            "score": score,
            "max_score": 5,
            "gross_margin": gross_margin,
            "operating_margin": operating_margin,
            "quality": quality,
        }