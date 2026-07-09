class OwnerEarningsAnalyzer:
    """
    Warren Buffett's Owner Earnings Analysis.
    """

    @staticmethod
    def _safe(value):
        return 0 if value is None else value

    def analyze(self, mapped):

        operating_cash_flow = self._safe(
            mapped.get("operating_cash_flow")
        )

        capital_expenditure = abs(
            self._safe(
                mapped.get("capital_expenditure")
            )
        )

        shares = self._safe(
            mapped.get("shares_outstanding")
        )

        market_cap = self._safe(
            mapped.get("market_cap")
        )

        current_price = mapped.get("current_price")

        owner_earnings = (
            operating_cash_flow
            - capital_expenditure
        )

        owner_earnings_per_share = None

        if shares > 0:
            owner_earnings_per_share = (
                owner_earnings / shares
            )

        owner_earnings_yield = None

        if market_cap > 0:
            owner_earnings_yield = (
                owner_earnings / market_cap
            ) * 100

        if owner_earnings_yield is None:
            quality = "Unknown"

        elif owner_earnings_yield >= 8:
            quality = "Excellent"

        elif owner_earnings_yield >= 5:
            quality = "Good"

        elif owner_earnings_yield >= 2:
            quality = "Average"

        else:
            quality = "Poor"

        return {
            "owner_earnings": owner_earnings,
            "owner_earnings_per_share": owner_earnings_per_share,
            "owner_earnings_yield": owner_earnings_yield,
            "quality": quality,
        }