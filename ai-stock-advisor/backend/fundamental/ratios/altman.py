class AltmanRatios:
    """
    Altman Z-Score calculations.

    Formula (Public Manufacturing Version):

    Z = 1.2*A
      + 1.4*B
      + 3.3*C
      + 0.6*D
      + 1.0*E
    """

    @staticmethod
    def working_capital_to_assets(
        current_assets,
        current_liabilities,
        total_assets,
    ):
        if (
            current_assets is None
            or current_liabilities is None
            or total_assets in (None, 0)
        ):
            return None

        return (
            current_assets - current_liabilities
        ) / total_assets

    @staticmethod
    def retained_earnings_to_assets(
        retained_earnings,
        total_assets,
    ):
        if (
            retained_earnings is None
            or total_assets in (None, 0)
        ):
            return None

        return retained_earnings / total_assets

    @staticmethod
    def ebit_to_assets(
        ebit,
        total_assets,
    ):
        if (
            ebit is None
            or total_assets in (None, 0)
        ):
            return None

        return ebit / total_assets

    @staticmethod
    def market_value_equity_to_liabilities(
        market_cap,
        total_liabilities,
    ):
        if (
            market_cap is None
            or total_liabilities in (None, 0)
        ):
            return None

        return market_cap / total_liabilities

    @staticmethod
    def sales_to_assets(
        revenue,
        total_assets,
    ):
        if (
            revenue is None
            or total_assets in (None, 0)
        ):
            return None

        return revenue / total_assets

    @staticmethod
    def z_score(
        a,
        b,
        c,
        d,
        e,
    ):
        if None in (a, b, c, d, e):
            return None

        return (
            1.2 * a
            + 1.4 * b
            + 3.3 * c
            + 0.6 * d
            + 1.0 * e
        )