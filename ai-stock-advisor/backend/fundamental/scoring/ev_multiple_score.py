class EVMultipleScore:
    """
    Scores Enterprise Value valuation.
    """

    @staticmethod
    def score(ev_to_ebitda):

        if ev_to_ebitda is None:
            return None

        if ev_to_ebitda <= 8:
            return 100

        elif ev_to_ebitda <= 10:
            return 90

        elif ev_to_ebitda <= 12:
            return 80

        elif ev_to_ebitda <= 15:
            return 65

        elif ev_to_ebitda <= 18:
            return 50

        elif ev_to_ebitda <= 25:
            return 30

        else:
            return 10