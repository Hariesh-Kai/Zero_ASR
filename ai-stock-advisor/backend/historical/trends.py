from typing import List, Optional


class TrendAnalyzer:
    """
    Analyzes the direction of historical financial values.
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

    def analyze(self, values: List[Optional[float]]):

        values = self._clean(values)

        if len(values) < 2:
            return {
                "trend": "Unknown",
                "change_percent": 0,
            }

        first = values[0]
        last = values[-1]

        if first == 0:
            change = 0
        else:
            change = ((last - first) / abs(first)) * 100

        if all(values[i] >= values[i - 1] for i in range(1, len(values))):
            trend = "Increasing"

        elif all(values[i] <= values[i - 1] for i in range(1, len(values))):
            trend = "Decreasing"

        else:
            trend = "Mixed"

        return {
            "trend": trend,
            "change_percent": round(change, 2),
            "years": len(values),
        }