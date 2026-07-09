class MagicFormulaScore:
    """
    Scores Joel Greenblatt Magic Formula.
    """

    @staticmethod
    def score(
        earnings_yield,
        return_on_capital,
    ):

        if (
            earnings_yield is None
            or return_on_capital is None
        ):
            return None

        score = 0

        # Earnings Yield
        if earnings_yield >= 10:
            score += 50

        elif earnings_yield >= 8:
            score += 40

        elif earnings_yield >= 6:
            score += 30

        elif earnings_yield >= 4:
            score += 20

        # Return on Capital
        if return_on_capital >= 30:
            score += 50

        elif return_on_capital >= 20:
            score += 40

        elif return_on_capital >= 15:
            score += 30

        elif return_on_capital >= 10:
            score += 20

        return score