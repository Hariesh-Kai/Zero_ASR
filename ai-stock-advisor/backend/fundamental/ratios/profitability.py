class ProfitabilityRatios:

    @staticmethod
    def gross_margin(gross_profit, revenue):

        if gross_profit is None or revenue in (None, 0):
            return None

        return (gross_profit / revenue) * 100


    @staticmethod
    def operating_margin(operating_income, revenue):

        if operating_income is None or revenue in (None, 0):
            return None

        return (operating_income / revenue) * 100


    @staticmethod
    def net_margin(net_income, revenue):

        if net_income is None or revenue in (None, 0):
            return None

        return (net_income / revenue) * 100


    @staticmethod
    def return_on_assets(net_income, total_assets):

        if net_income is None or total_assets in (None, 0):
            return None

        return (net_income / total_assets) * 100


    @staticmethod
    def return_on_equity(net_income, shareholder_equity):

        if net_income is None or shareholder_equity in (None, 0):
            return None

        return (net_income / shareholder_equity) * 100


    @staticmethod
    def return_on_capital_employed(
        ebit,
        total_assets,
        current_liabilities,
    ):

        if (
            ebit is None
            or total_assets is None
            or current_liabilities is None
        ):
            return None

        capital_employed = total_assets - current_liabilities

        if capital_employed == 0:
            return None

        return (ebit / capital_employed) * 100