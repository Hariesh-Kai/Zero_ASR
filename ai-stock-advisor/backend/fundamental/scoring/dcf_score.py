class DCFScore:
    """
    Scores a company based on its Discounted Cash Flow (DCF) valuation.
    """

    @staticmethod
    def score(
        intrinsic_value,
        current_price,
        margin_of_safety,
    ):

        if (
            intrinsic_value is None or
            current_price is None or
            margin_of_safety is None
        ):
            return None

        if margin_of_safety >= 50:
            return 100

        elif margin_of_safety >= 30:
            return 90

        elif margin_of_safety >= 20:
            return 80

        elif margin_of_safety >= 10:
            return 70

        elif margin_of_safety >= 0:
            return 60

        elif margin_of_safety >= -10:
            return 40

        elif margin_of_safety >= -20:
            return 20

        else:
            return 0