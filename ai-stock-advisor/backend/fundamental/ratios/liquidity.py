class LiquidityRatios:

    @staticmethod
    def current_ratio(current_assets, current_liabilities):

        if (
            current_assets in (None, "")
            or current_liabilities in (None, "")
            or current_liabilities == 0
        ):
            return None

        return current_assets / current_liabilities

    @staticmethod
    def quick_ratio(current_assets, inventory, current_liabilities):

        if inventory in (None, ""):
            inventory = 0

        if (
            current_assets in (None, "")
            or current_liabilities in (None, "")
            or current_liabilities == 0
        ):
            return None

        return (current_assets - inventory) / current_liabilities

    @staticmethod
    def cash_ratio(cash, current_liabilities):

        if (
            cash in (None, "")
            or current_liabilities in (None, "")
            or current_liabilities == 0
        ):
            return None

        return cash / current_liabilities