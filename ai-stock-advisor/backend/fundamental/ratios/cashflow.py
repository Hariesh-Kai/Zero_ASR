class CashFlowRatios:
    """
    Cash Flow ratio calculations.
    """

    @staticmethod
    def operating_cash_flow_ratio(
        operating_cash_flow,
        current_liabilities,
    ):
        if operating_cash_flow is None or current_liabilities in (None, 0):
            return None

        return operating_cash_flow / current_liabilities

    @staticmethod
    def free_cash_flow(
        operating_cash_flow,
        capital_expenditure,
    ):
        if operating_cash_flow is None or capital_expenditure is None:
            return None

        return operating_cash_flow - abs(capital_expenditure)

    @staticmethod
    def cash_conversion_ratio(
        operating_cash_flow,
        net_income,
    ):
        if operating_cash_flow is None or net_income in (None, 0):
            return None

        return operating_cash_flow / net_income