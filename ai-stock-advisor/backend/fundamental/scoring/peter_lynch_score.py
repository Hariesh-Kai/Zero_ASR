class PeterLynchScore:
    """
    Scores the Peter Lynch Fair Value analysis.
    """

    @staticmethod
    def score(upside):

        if upside is None:
            return None

        if upside >= 50:
            return 100

        elif upside >= 30:
            return 90

        elif upside >= 20:
            return 80

        elif upside >= 10:
            return 70

        elif upside >= 0:
            return 60

        elif upside >= -10:
            return 50

        elif upside >= -20:
            return 40

        elif upside >= -30:
            return 30

        elif upside >= -50:
            return 20

        return 10