class FinancialHealthScore:
    """
    Scores financial health.
    Maximum Score: 100
    """

    @staticmethod
    def score(
        interest_coverage,
        debt_to_ebitda,
        financial_leverage,
    ):

        score = 0

        # Interest Coverage (40)
        if interest_coverage is not None:
            if interest_coverage >= 10:
                score += 40
            elif interest_coverage >= 5:
                score += 30
            elif interest_coverage >= 2:
                score += 20

        # Debt / EBITDA (30)
        if debt_to_ebitda is not None:
            if debt_to_ebitda < 2:
                score += 30
            elif debt_to_ebitda < 3:
                score += 20
            elif debt_to_ebitda < 5:
                score += 10

        # Financial Leverage (30)
        if financial_leverage is not None:
            if financial_leverage < 2:
                score += 30
            elif financial_leverage < 3:
                score += 20
            elif financial_leverage < 5:
                score += 10

        return score