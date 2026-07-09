class EconomicMoatScore:
    """
    Scores the Economic Moat.
    """

    @staticmethod
    def score(score):

        if score is None:
            return None

        if score == 4:
            return 100

        elif score == 3:
            return 80

        elif score == 2:
            return 60

        elif score == 1:
            return 30

        return 0