class GrowthScore:
    """
    Scores company growth.
    Maximum Score: 100
    """

    @staticmethod
    def score(
        revenue_growth,
        earnings_growth,
        eps_growth,
    ):

        score = 0

        # Revenue Growth (40)
        if revenue_growth is not None:
            if revenue_growth >= 20:
                score += 40
            elif revenue_growth >= 15:
                score += 30
            elif revenue_growth >= 10:
                score += 20
            elif revenue_growth >= 5:
                score += 10

        # Earnings Growth (30)
        if earnings_growth is not None:
            if earnings_growth >= 20:
                score += 30
            elif earnings_growth >= 15:
                score += 25
            elif earnings_growth >= 10:
                score += 20
            elif earnings_growth >= 5:
                score += 10

        # EPS Growth (30)
        if eps_growth is not None:
            if eps_growth >= 20:
                score += 30
            elif eps_growth >= 15:
                score += 25
            elif eps_growth >= 10:
                score += 20
            elif eps_growth >= 5:
                score += 10

        return score