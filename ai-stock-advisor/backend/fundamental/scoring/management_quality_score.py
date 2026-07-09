class ManagementQualityScore:
    """
    Converts Management Quality score
    into a 0-100 score.
    """

    @staticmethod
    def score(score):

        if score is None:
            return None

        if score == 5:
            return 100

        elif score == 4:
            return 80

        elif score == 3:
            return 60

        elif score == 2:
            return 40

        elif score == 1:
            return 20

        return 0