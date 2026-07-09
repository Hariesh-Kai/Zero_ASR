class BeneishScore:
    """
    Scores the Beneish M-Score.
    Maximum Score: 100
    """

    @staticmethod
    def score(m_score):

        if m_score is None:
            return None

        # Very Low Manipulation Risk
        if m_score <= -2.50:
            return 100

        # Low Risk
        elif m_score <= -2.22:
            return 90

        # Slight Risk
        elif m_score <= -2.00:
            return 70

        # Moderate Risk
        elif m_score <= -1.78:
            return 50

        # High Risk
        elif m_score <= -1.50:
            return 30

        # Very High Risk
        else:
            return 10