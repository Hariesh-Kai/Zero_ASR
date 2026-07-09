class OwnerEarningsScore:
    """
    Scores Warren Buffett Owner Earnings.
    """

    @staticmethod
    def score(owner_earnings_yield):

        if owner_earnings_yield is None:
            return None

        if owner_earnings_yield >= 10:
            return 100

        elif owner_earnings_yield >= 8:
            return 90

        elif owner_earnings_yield >= 6:
            return 80

        elif owner_earnings_yield >= 4:
            return 70

        elif owner_earnings_yield >= 2:
            return 50

        elif owner_earnings_yield >= 0:
            return 30

        else:
            return 0