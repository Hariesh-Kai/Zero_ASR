class ReinvestmentRateAnalyzer:
    """
    Measures how much cash flow is reinvested
    back into the business.
    """

    @staticmethod
    def _safe(value):
        return 0 if value is None else value

    def analyze(self, mapped):

        operating_cash_flow = self._safe(
            mapped.get("operating_cash_flow")
        )

        capital_expenditure = abs(
            self._safe(
                mapped.get("capital_expenditure")
            )
        )

        reinvestment_rate = 0

        if operating_cash_flow > 0:
            reinvestment_rate = (
                capital_expenditure
                / operating_cash_flow
            ) * 100

        score = 1

        if (
            reinvestment_rate >= 20
            and reinvestment_rate <= 50
        ):
            score = 5

        elif (
            reinvestment_rate >= 15
            and reinvestment_rate < 20
        ):
            score = 4

        elif (
            reinvestment_rate > 50
            and reinvestment_rate <= 70
        ):
            score = 4

        elif (
            reinvestment_rate >= 10
            and reinvestment_rate < 15
        ):
            score = 3

        elif (
            reinvestment_rate > 70
            and reinvestment_rate <= 90
        ):
            score = 3

        elif (
            reinvestment_rate >= 5
            and reinvestment_rate < 10
        ):
            score = 2

        elif reinvestment_rate > 90:
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
            "reinvestment_rate": reinvestment_rate,
            "quality": quality,
        }