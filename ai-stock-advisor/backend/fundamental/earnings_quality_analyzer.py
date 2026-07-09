class EarningsQualityAnalyzer:
    """
    Measures whether reported earnings are supported
    by operating cash flow.

    High-quality earnings generally have operating cash flow
    greater than or equal to net income.
    """

    @staticmethod
    def _safe(value):
        return 0 if value is None else value

    def analyze(self, mapped):

        operating_cash_flow = self._safe(
            mapped.get("operating_cash_flow")
        )

        net_income = self._safe(
            mapped.get("net_income")
        )

        accrual_ratio = 0

        if net_income != 0:
            accrual_ratio = (
                operating_cash_flow - net_income
            ) / net_income

        score = 1

        if accrual_ratio >= 0.50:
            score = 5

        elif accrual_ratio >= 0.25:
            score = 4

        elif accrual_ratio >= 0.10:
            score = 3

        elif accrual_ratio >= 0:
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
            "operating_cash_flow": operating_cash_flow,
            "net_income": net_income,
            "accrual_ratio": accrual_ratio,
            "quality": quality,
        }