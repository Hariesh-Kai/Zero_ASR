class LeverageRatios:

    @staticmethod
    def debt_to_equity(
        total_debt,
        shareholder_equity,
    ):

        if shareholder_equity == 0:
            return None

        return total_debt / shareholder_equity


    @staticmethod
    def debt_to_assets(
        total_debt,
        total_assets,
    ):

        if total_assets == 0:
            return None

        return total_debt / total_assets


    @staticmethod
    def equity_ratio(
        shareholder_equity,
        total_assets,
    ):

        if total_assets == 0:
            return None

        return shareholder_equity / total_assets