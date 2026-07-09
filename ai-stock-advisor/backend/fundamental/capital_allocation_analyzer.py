class CapitalAllocationAnalyzer:
    """
    Evaluates management's capital allocation efficiency.
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

        free_cash_flow = self._safe(
            mapped.get("free_cash_flow")
        )

        capex_ratio = 0

        if operating_cash_flow > 0:
            capex_ratio = (
                capital_expenditure
                / operating_cash_flow
            ) * 100

        fcf_conversion = 0

        if operating_cash_flow > 0:
            fcf_conversion = (
                free_cash_flow
                / operating_cash_flow
            ) * 100

        score = 1

        if (
            capex_ratio < 40
            and fcf_conversion > 60
        ):
            score = 5

        elif (
            capex_ratio < 50
            and fcf_conversion > 50
        ):
            score = 4

        elif (
            capex_ratio < 60
            and fcf_conversion > 40
        ):
            score = 3

        elif (
            capex_ratio < 80
            and fcf_conversion > 20
        ):
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
            "capex_ratio": capex_ratio,
            "fcf_conversion": fcf_conversion,
            "quality": quality,
        }