class ShareholderYieldAnalyzer:
    """
    Measures total capital returned to shareholders.

    Shareholder Yield =
        Dividend Yield
      + Buyback Yield
      - Dilution Yield
    """

    @staticmethod
    def _safe(value):
        return 0 if value is None else value

    def analyze(
        self,
        profile,
        mapped,
        previous_mapped,
    ):

        dividend_yield = self._safe(
            profile.get("dividend_yield")
        )

        current_shares = self._safe(
            mapped.get("shares_outstanding")
        )

        previous_shares = self._safe(
            previous_mapped.get("shares_outstanding")
        )

        # ----------------------------------------------------
        # Buyback Yield
        # ----------------------------------------------------

        buyback_yield = 0

        if (
            current_shares > 0
            and previous_shares > 0
        ):

            buyback_yield = (
                (previous_shares - current_shares)
                / previous_shares
            ) * 100

        # Ignore tiny changes in shares outstanding
        # (<0.1%) since they are usually caused by
        # employee stock compensation, option exercises,
        # or normal accounting adjustments.
        if abs(buyback_yield) < 0.1:
            buyback_yield = 0

        # ----------------------------------------------------
        # Shareholder Yield
        # ----------------------------------------------------

        shareholder_yield = (
            dividend_yield
            + buyback_yield
        )

        # ----------------------------------------------------
        # Score
        # ----------------------------------------------------

        score = 1

        if shareholder_yield >= 8:
            score = 5

        elif shareholder_yield >= 5:
            score = 4

        elif shareholder_yield >= 2:
            score = 3

        elif shareholder_yield >= 0.5:
            score = 2

        # ----------------------------------------------------
        # Quality
        # ----------------------------------------------------

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
            "dividend_yield": dividend_yield,
            "buyback_yield": buyback_yield,
            "shareholder_yield": shareholder_yield,
            "quality": quality,
        }