class PricingPowerAnalyzer:
    """
    Evaluates a company's pricing power
    using gross and operating margins.
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

        gross_profit = self._safe(
            mapped.get("gross_profit")
        )

        operating_income = self._safe(
            mapped.get("operating_income")
        )

        gross_margin = 0
        operating_margin = 0

        if revenue > 0:
            gross_margin = (
                gross_profit / revenue
            ) * 100

            operating_margin = (
                operating_income / revenue
            ) * 100

        score = 1

        if gross_margin >= 60 and operating_margin >= 25:
            score = 5

        elif gross_margin >= 50 and operating_margin >= 20:
            score = 4

        elif gross_margin >= 40 and operating_margin >= 15:
            score = 3

        elif gross_margin >= 30 and operating_margin >= 10:
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
            "gross_margin": gross_margin,
            "operating_margin": operating_margin,
            "quality": quality,
        }