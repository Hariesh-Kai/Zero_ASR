class EfficiencyRatios:
    """
    Efficiency ratio calculations.
    """

    @staticmethod
    def asset_turnover(revenue, total_assets):

        if revenue is None or total_assets in (None, 0):
            return None

        return revenue / total_assets

    @staticmethod
    def inventory_turnover(cost_of_revenue, inventory):

        if cost_of_revenue is None or inventory in (None, 0):
            return None

        return cost_of_revenue / inventory

    @staticmethod
    def receivables_turnover(revenue, accounts_receivable):

        if revenue is None or accounts_receivable in (None, 0):
            return None

        return revenue / accounts_receivable

    @staticmethod
    def working_capital_turnover(
        revenue,
        current_assets,
        current_liabilities,
    ):

        if (
            revenue is None
            or current_assets is None
            or current_liabilities is None
        ):
            return None

        working_capital = current_assets - current_liabilities

        if working_capital == 0:
            return None

        return revenue / working_capital