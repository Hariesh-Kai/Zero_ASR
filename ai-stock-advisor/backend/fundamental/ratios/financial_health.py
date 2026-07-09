class FinancialHealthRatios:
    """
    Financial health related ratios.
    """

    @staticmethod
    def _to_number(value):
        """
        Convert values to float.
        Returns None for invalid values.
        """
        if value in (None, "", "N/A"):
            return None

        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def interest_coverage(ebit, interest_expense):

        ebit = FinancialHealthRatios._to_number(ebit)
        interest_expense = FinancialHealthRatios._to_number(
            interest_expense
        )

        if (
            ebit is None
            or interest_expense is None
            or interest_expense == 0
        ):
            return None

        return ebit / abs(interest_expense)

    @staticmethod
    def debt_to_ebitda(total_debt, ebitda):

        total_debt = FinancialHealthRatios._to_number(
            total_debt
        )

        ebitda = FinancialHealthRatios._to_number(
            ebitda
        )

        if (
            total_debt is None
            or ebitda is None
            or ebitda == 0
        ):
            return None

        return total_debt / ebitda

    @staticmethod
    def financial_leverage(
        total_assets,
        shareholder_equity,
    ):

        total_assets = FinancialHealthRatios._to_number(
            total_assets
        )

        shareholder_equity = FinancialHealthRatios._to_number(
            shareholder_equity
        )

        if (
            total_assets is None
            or shareholder_equity is None
            or shareholder_equity == 0
        ):
            return None

        return total_assets / shareholder_equity