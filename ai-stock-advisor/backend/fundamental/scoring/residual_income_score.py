class ResidualIncomeScore:
    """
    Converts Residual Income valuation
    into a 0-100 score.
    """

    @staticmethod
    def score(valuation):

        if valuation is None:
            return None

        if valuation == "Undervalued":
            return 100

        elif valuation == "Fair":
            return 60

        elif valuation == "Overvalued":
            return 20

        return 0    