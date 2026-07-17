
from typing import List, Optional


class GrowthAnalyzer:
    """
    Calculates long-term growth metrics.
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

    def cagr(self, values: List[Optional[float]]):

        values = self._clean(values)

        if len(values) < 2:
            return None

        first = values[0]
        last = values[-1]

        if first <= 0:
            return None

        years = len(values) - 1

        cagr = ((last / first) ** (1 / years) - 1) * 100

        return round(cagr, 2)

    def analyze(
        self,
        revenue,
        net_income,
        free_cash_flow,
        book_value,
    ):

        return {

            "revenue_cagr": self.cagr(revenue),

            "earnings_cagr": self.cagr(net_income),

            "free_cash_flow_cagr": self.cagr(
                free_cash_flow
            ),

            "book_value_cagr": self.cagr(
                book_value
            ),
        }