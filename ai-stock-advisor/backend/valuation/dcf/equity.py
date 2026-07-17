class EquityValue:
    """
    Converts Enterprise Value into
    Equity Value and Intrinsic Value.
    """

    def calculate(

        self,

        enterprise_value,

        company,

    ):

        cash = company.get(
            "total_cash",
            0,
        ) or 0

        debt = company.get(
            "total_debt",
            0,
        ) or 0

        shares = company.get(

            "shares_outstanding",

            1,

        ) or 1

        current_price = company.get(

            "current_price",

            0,

        ) or 0

        equity_value = (

            enterprise_value

            + cash

            - debt

        )

        intrinsic = (

            equity_value

            / shares

        )

        if current_price > 0:

            upside = (

                (intrinsic - current_price)

                / current_price

            ) * 100

        else:

            upside = 0

        return {

            "cash": cash,

            "debt": debt,

            "shares": shares,

            "equity_value": round(

                equity_value,

                2,

            ),

            "intrinsic_value": round(

                intrinsic,

                2,

            ),

            "upside": round(

                upside,

                2,

            ),

        }