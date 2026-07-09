class DebtMaturityAnalyzer:
    """
    Evaluates the company's long-term debt burden
    relative to its total debt.
    """

    @staticmethod
    def _safe(value):
        return 0 if value is None else value

    def analyze(
        self,
        mapped,
    ):

        total_debt = self._safe(
            mapped.get("total_debt")
        )

        current_liabilities = self._safe(
            mapped.get("current_liabilities")
        )

        long_term_debt = max(
            0,
            total_debt - current_liabilities
        )

        long_term_ratio = 0

        if total_debt > 0:
            long_term_ratio = (
                long_term_debt
                / total_debt
            ) * 100

        score = 1

        if long_term_ratio <= 20:
            score = 5

        elif long_term_ratio <= 40:
            score = 4

        elif long_term_ratio <= 60:
            score = 3

        elif long_term_ratio <= 80:
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
            "long_term_debt": long_term_debt,
            "long_term_debt_ratio": long_term_ratio,
            "quality": quality,
        }