class MarketLeadershipAnalyzer:
    """
    Evaluates market leadership using
    market capitalization and revenue.
    """

    @staticmethod
    def _safe(value):
        return 0 if value is None else value

    def analyze(
        self,
        mapped,
    ):

        market_cap = self._safe(
            mapped.get("market_cap")
        )

        revenue = self._safe(
            mapped.get("revenue")
        )

        score = 1

        if market_cap >= 200_000_000_000:
            score = 5

        elif market_cap >= 50_000_000_000:
            score = 4

        elif market_cap >= 10_000_000_000:
            score = 3

        elif market_cap >= 2_000_000_000:
            score = 2

        else:
            score = 1

        if score == 5:
            leadership = "Dominant"

        elif score == 4:
            leadership = "Leader"

        elif score == 3:
            leadership = "Strong"

        elif score == 2:
            leadership = "Emerging"

        else:
            leadership = "Small"

        return {
            "score": score,
            "max_score": 5,
            "market_cap": market_cap,
            "revenue": revenue,
            "leadership": leadership,
        }