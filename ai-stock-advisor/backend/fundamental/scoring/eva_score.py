class EVAScore:
    """
    Converts EVA quality
    into a 0-100 score.
    """

    @staticmethod
    def score(quality):

        if quality is None:
            return None

        if quality == "Value Creator":
            return 100

        elif quality == "Value Destroyer":
            return 20

        return 0