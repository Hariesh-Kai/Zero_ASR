from typing import List, Optional


class QualityAnalyzer:
    """
    Evaluates the consistency of historical financial metrics.
    """

    @staticmethod
    def _clean(values: List[Optional[float]]) -> List[float]:

        cleaned = []

        for value in values:

            if value in (None, "", "N/A"):
                continue

            try:
                cleaned.append(float(value))
            except (TypeError, ValueError):
                continue

        return cleaned

    @staticmethod
    def _consistency_score(values: List[float]):

        if len(values) < 2:
            return "Unknown"

        increases = 0

        for i in range(1, len(values)):
            if values[i] >= values[i - 1]:
                increases += 1

        ratio = increases / (len(values) - 1)

        if ratio >= 0.90:
            return "Excellent"

        elif ratio >= 0.70:
            return "Good"

        elif ratio >= 0.50:
            return "Average"

        return "Weak"

    def analyze(
        self,
        revenue,
        earnings,
        free_cash_flow,
        roe,
        roic,
    ):

        revenue = self._clean(revenue)
        earnings = self._clean(earnings)
        free_cash_flow = self._clean(free_cash_flow)
        roe = self._clean(roe)
        roic = self._clean(roic)

        return {

            "revenue_quality":
                self._consistency_score(revenue),

            "earnings_quality":
                self._consistency_score(earnings),

            "cashflow_quality":
                self._consistency_score(free_cash_flow),

            "roe_quality":
                self._consistency_score(roe),

            "roic_quality":
                self._consistency_score(roic),
        }