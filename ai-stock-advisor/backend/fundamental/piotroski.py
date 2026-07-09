class PiotroskiFScore:
    """
    Calculates the Piotroski F-Score (0-9).

    Uses current and previous historical analysis.
    """

    def calculate(
        self,
        current,
        previous,
    ):

        score = 0

        # =====================================================
        # PROFITABILITY
        # =====================================================

        # Positive Net Income
        if (current["net_income"] or 0) > 0:
            score += 1

        # Positive Operating Cash Flow
        if (current["operating_cash_flow"] or 0) > 0:
            score += 1

        # Higher ROA
        current_roa = current["profitability"]["roa"]
        previous_roa = previous["profitability"]["roa"]

        if (
            current_roa is not None
            and previous_roa is not None
            and current_roa > previous_roa
        ):
            score += 1

        # Operating Cash Flow > Net Income
        if (
            (current["operating_cash_flow"] or 0)
            >
            (current["net_income"] or 0)
        ):
            score += 1

        # =====================================================
        # LEVERAGE / LIQUIDITY
        # =====================================================

        current_debt = current["total_debt"]
        previous_debt = previous["total_debt"]

        if (
            current_debt is not None
            and previous_debt is not None
            and current_debt < previous_debt
        ):
            score += 1

        current_ratio = current["liquidity"]["current_ratio"]
        previous_ratio = previous["liquidity"]["current_ratio"]

        if (
            current_ratio is not None
            and previous_ratio is not None
            and current_ratio > previous_ratio
        ):
            score += 1

        current_shares = current["shares_outstanding"]
        previous_shares = previous["shares_outstanding"]

        if (
            current_shares is not None
            and previous_shares is not None
            and current_shares <= previous_shares
        ):
            score += 1

        # =====================================================
        # OPERATING EFFICIENCY
        # =====================================================

        current_margin = current["profitability"]["gross_margin"]
        previous_margin = previous["profitability"]["gross_margin"]

        if (
            current_margin is not None
            and previous_margin is not None
            and current_margin > previous_margin
        ):
            score += 1

        current_turnover = current["efficiency"]["asset_turnover"]
        previous_turnover = previous["efficiency"]["asset_turnover"]

        if (
            current_turnover is not None
            and previous_turnover is not None
            and current_turnover > previous_turnover
        ):
            score += 1

        # =====================================================
        # Rating
        # =====================================================

        if score >= 8:
            rating = "Excellent"
        elif score >= 6:
            rating = "Good"
        elif score >= 4:
            rating = "Average"
        else:
            rating = "Weak"

        return {
            "score": score,
            "max_score": 9,
            "rating": rating,
        }