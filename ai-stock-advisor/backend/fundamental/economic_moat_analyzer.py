class EconomicMoatAnalyzer:
    """
    Estimates whether a company has a durable competitive advantage
    (Economic Moat).
    """

    @staticmethod
    def _safe(value):
        return 0 if value is None else value

    def analyze(
        self,
        profitability,
        leverage,
    ):

        roe = self._safe(
            profitability.get("roe")
        )

        gross_margin = self._safe(
            profitability.get("gross_margin")
        )

        operating_margin = self._safe(
            profitability.get("operating_margin")
        )

        debt_to_equity = self._safe(
            leverage.get("debt_to_equity")
        )

        score = 0

        # High ROE
        if roe >= 20:
            score += 1

        # High Gross Margin
        if gross_margin >= 50:
            score += 1

        # Strong Operating Margin
        if operating_margin >= 20:
            score += 1

        # Low Debt
        if debt_to_equity <= 0.5:
            score += 1

        # Final Rating
        if score == 4:
            moat = "Wide"

        elif score == 3:
            moat = "Narrow"

        elif score == 2:
            moat = "Moderate"

        else:
            moat = "None"

        return {
            "score": score,
            "max_score": 4,
            "roe": roe,
            "gross_margin": gross_margin,
            "operating_margin": operating_margin,
            "debt_to_equity": debt_to_equity,
            "moat": moat,
        }