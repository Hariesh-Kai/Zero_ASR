class WACC:
    """
    Calculates the Weighted Average Cost of Capital.
    """

    def calculate(
        self,
        assumptions,
    ):

        rf = assumptions["risk_free_rate"]

        beta = assumptions["beta"]

        market = assumptions["market_return"]

        cost_of_equity = rf + beta * (

            market - rf

        )

        after_tax_debt = (

            assumptions["cost_of_debt"]

            * (1 - assumptions["tax_rate"])

        )

        wacc = (

            assumptions["equity_ratio"]

            * cost_of_equity

        ) + (

            assumptions["debt_ratio"]

            * after_tax_debt

        )

        return {

            "cost_of_equity": round(

                cost_of_equity,

                4,

            ),

            "after_tax_debt": round(

                after_tax_debt,

                4,

            ),

            "wacc": round(

                wacc,

                4,

            ),

        }