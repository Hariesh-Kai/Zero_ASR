class OwnerEarningsModel:
    """
    Buffett Owner Earnings Valuation.
    """

    def analyze(
        self,
        data,
    ):

        company = data["company"]

        cashflow = data["cash_flow"]

        current_price = company.get(
            "current_price"
        )

        operating_cashflow = cashflow.get(
            "operating_cash_flow"
        )

        shares = company.get(
            "shares_outstanding"
        )

        capex = abs(

            cashflow.get(
                "capital_expenditure",
                0,
            )

            or 0

        )

        if not all([

            current_price,

            operating_cashflow,

            shares,

        ]):

            return {

                "model": "Owner Earnings",

                "fair_value": None,

                "current_price": current_price,

                "margin_of_safety": None,

                "status": "Unavailable",

            }

        # ----------------------------------
        # Buffett Owner Earnings
        # ----------------------------------

        owner_earnings = (

            operating_cashflow

            - capex

        )

        multiple = 15

        equity_value = (

            owner_earnings

            * multiple

        )

        fair_value = (

            equity_value

            / shares

        )

        margin = (

            (fair_value - current_price)

            / current_price

        ) * 100

        if margin > 20:

            status = "Undervalued"

        elif margin < -20:

            status = "Overvalued"

        else:

            status = "Fair Value"

        return {

            "model": "Owner Earnings",

            "fair_value": round(
                fair_value,
                2,
            ),

            "current_price": round(
                current_price,
                2,
            ),

            "margin_of_safety": round(
                margin,
                2,
            ),

            "status": status,

        }