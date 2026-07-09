class InterestRateRiskAnalyzer:
    """
    Evaluates the company's exposure to
    rising interest rates.
    """

    @staticmethod
    def _safe(value):
        if value in (None, "", "N/A"):
            return 0.0

        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    def analyze(
        self,
        mapped,
    ):

        interest_expense = self._safe(
            mapped.get("interest_expense")
        )

        total_debt = self._safe(
            mapped.get("total_debt")
        )

        risk_ratio = 0.0

        if total_debt > 0:
            risk_ratio = (
                interest_expense
                / total_debt
            ) * 100

        if risk_ratio <= 2:
            score = 5
        elif risk_ratio <= 4:
            score = 4
        elif risk_ratio <= 6:
            score = 3
        elif risk_ratio <= 8:
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
            "interest_expense": interest_expense,
            "total_debt": total_debt,
            "interest_rate_risk": risk_ratio,
            "quality": quality,
        }