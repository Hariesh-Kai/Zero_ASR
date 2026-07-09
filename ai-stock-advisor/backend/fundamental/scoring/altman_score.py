class AltmanScore:
    """
    Scores the Altman Z-Score.

    Maximum Score: 100

    Interpretation:
    > 2.99  : Safe Zone
    1.81-2.99 : Grey Zone
    < 1.81 : Distress Zone
    """

    @staticmethod
    def score(z_score):

        if z_score is None:
            return None

        # Safe Zone
        if z_score >= 5:
            return 100

        elif z_score >= 4:
            return 95

        elif z_score >= 3:
            return 90

        # Grey Zone
        elif z_score >= 2.7:
            return 80

        elif z_score >= 2.4:
            return 70

        elif z_score >= 2.1:
            return 60

        elif z_score >= 1.81:
            return 50

        # Distress Zone
        elif z_score >= 1.5:
            return 35

        elif z_score >= 1.2:
            return 20

        elif z_score >= 1.0:
            return 10

        else:
            return 0