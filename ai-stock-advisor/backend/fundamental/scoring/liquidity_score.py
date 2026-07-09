class LiquidityScore:
    """
    Scores liquidity ratios.
    Maximum Score: 100
    """

    @staticmethod
    def score(
        current_ratio,
        quick_ratio,
        cash_ratio,
    ):

        score = 0

        # Current Ratio (40)
        if current_ratio is not None:
            if current_ratio >= 2:
                score += 40
            elif current_ratio >= 1.5:
                score += 30
            elif current_ratio >= 1:
                score += 20

        # Quick Ratio (35)
        if quick_ratio is not None:
            if quick_ratio >= 1.5:
                score += 35
            elif quick_ratio >= 1:
                score += 25
            elif quick_ratio >= 0.8:
                score += 15

        # Cash Ratio (25)
        if cash_ratio is not None:
            if cash_ratio >= 1:
                score += 25
            elif cash_ratio >= 0.5:
                score += 15
            elif cash_ratio >= 0.25:
                score += 10

        return score