class BuffettAnalyzer:
    """
    Warren Buffett Quality Analysis.

    Evaluates business quality using Buffett-style metrics.
    """

    @staticmethod
    def _safe(value):
        if value in (None, "", "N/A"):
            return 0

        try:
            return float(value)
        except (TypeError, ValueError):
            return 0

    def analyze(self, mapped):

        revenue = self._safe(mapped.get("revenue"))
        net_income = self._safe(mapped.get("net_income"))
        shareholder_equity = self._safe(mapped.get("shareholder_equity"))
        total_debt = self._safe(mapped.get("total_debt"))
        operating_cash_flow = self._safe(mapped.get("operating_cash_flow"))
        interest_expense = self._safe(mapped.get("interest_expense"))
        ebit = self._safe(mapped.get("ebit"))
        gross_profit = self._safe(mapped.get("gross_profit"))

        score = 0

        # ROE
        roe = 0
        if shareholder_equity > 0:
            roe = (net_income / shareholder_equity) * 100
            if roe >= 15:
                score += 1

        # Debt
        debt_to_equity = 0
        if shareholder_equity > 0:
            debt_to_equity = total_debt / shareholder_equity
            if debt_to_equity < 0.5:
                score += 1

        # Gross Margin
        gross_margin = 0
        if revenue > 0:
            gross_margin = (gross_profit / revenue) * 100
            if gross_margin >= 40:
                score += 1

        # Cash Generation
        if operating_cash_flow > net_income:
            score += 1

        # Interest Coverage
        interest_coverage = 0
        if interest_expense > 0:
            interest_coverage = ebit / interest_expense
            if interest_coverage >= 8:
                score += 1

        if score == 5:
            quality = "Excellent"

        elif score >= 4:
            quality = "Very Good"

        elif score >= 3:
            quality = "Good"

        elif score >= 2:
            quality = "Average"

        else:
            quality = "Poor"

        return {
            "score": score,
            "max_score": 5,
            "roe": roe,
            "debt_to_equity": debt_to_equity,
            "gross_margin": gross_margin,
            "interest_coverage": interest_coverage,
            "quality": quality,
        }