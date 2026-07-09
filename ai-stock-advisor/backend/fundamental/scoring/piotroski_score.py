class PiotroskiScore:
    """
    Converts Piotroski F-Score into a standardized score (0-100).
    """

    @staticmethod
    def score(
        piotroski_score,
    ):

        if piotroski_score is None:
            return None

        if piotroski_score >= 9:
            return 100

        elif piotroski_score == 8:
            return 95

        elif piotroski_score == 7:
            return 90

        elif piotroski_score == 6:
            return 80

        elif piotroski_score == 5:
            return 70

        elif piotroski_score == 4:
            return 60

        elif piotroski_score == 3:
            return 45

        elif piotroski_score == 2:
            return 30

        elif piotroski_score == 1:
            return 15

        return 0