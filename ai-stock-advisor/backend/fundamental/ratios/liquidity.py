class LiquidityRatios:

    @staticmethod
    def current_ratio(current_assets, current_liabilities):

        if current_assets is None:
            return None

        if current_liabilities is None:
            return None

        if current_liabilities == 0:
            return None

        return current_assets / current_liabilities


    @staticmethod
    def quick_ratio(current_assets, inventory, current_liabilities):

        if (
            current_assets is None
            or inventory is None
            or current_liabilities is None
            or current_liabilities == 0
        ):
            return None

        return (current_assets - inventory) / current_liabilities


    @staticmethod
    def cash_ratio(cash, current_liabilities):

        if (
            cash is None
            or current_liabilities is None
            or current_liabilities == 0
        ):
            return None

        return cash / current_liabilities