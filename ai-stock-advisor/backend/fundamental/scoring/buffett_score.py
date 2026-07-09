class BuffettScore:
    """
    Converts Buffett Quality Score into a 0-100 score.
    """

    @staticmethod
    def score(score):

        if score is None:
            return None

        if score == 5:
            return 100

        elif score == 4:
            return 85

        elif score == 3:
            return 70

        elif score == 2:
            return 50

        elif score == 1:
            return 25

        else:
            return 0