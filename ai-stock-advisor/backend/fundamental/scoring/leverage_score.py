class LeverageScore:
    """
    Scores company leverage.
    Maximum Score: 100
    """

    @staticmethod
    def score(
        debt_to_equity,
        debt_to_assets,
        equity_ratio,
    ):

        score = 0

        # Debt to Equity (40)
        if debt_to_equity is not None:
            if debt_to_equity <= 0.5:
                score += 40
            elif debt_to_equity <= 1:
                score += 30
            elif debt_to_equity <= 2:
                score += 20
            else:
                score += 10

        # Debt to Assets (30)
        if debt_to_assets is not None:
            if debt_to_assets <= 0.30:
                score += 30
            elif debt_to_assets <= 0.50:
                score += 20
            elif debt_to_assets <= 0.70:
                score += 10

        # Equity Ratio (30)
        if equity_ratio is not None:
            if equity_ratio >= 0.60:
                score += 30
            elif equity_ratio >= 0.40:
                score += 20
            elif equity_ratio >= 0.20:
                score += 10

        return score