class DebtServiceCoverageAnalyzer:
    """
    Measures the company's ability to cover
    its debt using operating cash flow.
    """

    @staticmethod
    def _safe(value):
        return 0 if value is None else value

    def analyze(
        self,
        mapped,
    ):

        operating_cash_flow = self._safe(
            mapped.get("operating_cash_flow")
        )

        total_debt = self._safe(
            mapped.get("total_debt")
        )

        coverage = 0

        if total_debt > 0:
            coverage = (
                operating_cash_flow
                / total_debt
            )

        score = 1

        if coverage >= 2:
            score = 5

        elif coverage >= 1.5:
            score = 4

        elif coverage >= 1:
            score = 3

        elif coverage >= 0.5:
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
            "debt_service_coverage": coverage,
            "operating_cash_flow": operating_cash_flow,
            "total_debt": total_debt,
            "quality": quality,
        }