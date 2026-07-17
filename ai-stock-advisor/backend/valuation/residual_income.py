class ResidualIncomeModel:
    """
    Residual Income Valuation Model.
    """

    def analyze(
        self,
        data,
    ):

        company = data["company"]

        current_price = company.get(
            "current_price"
        )

        book_value = company.get(
            "book_value"
        )

        roe = company.get(
            "return_on_equity"
        )

        shares = company.get(
            "shares_outstanding"
        )

        if not all([

            current_price,

            book_value,

            roe,

            shares,

        ]):

            return {

                "model": "Residual Income",

                "fair_value": None,

                "current_price": current_price,

                "margin_of_safety": None,

                "status": "Unavailable",

            }

        cost_of_equity = 0.10

        residual = (

            book_value *

            (roe - cost_of_equity)

        )

        fair_value = (

            book_value +

            residual

        )

        margin = (

            (fair_value - current_price)

            /

            current_price

        ) * 100

        if margin > 20:

            status = "Undervalued"

        elif margin < -20:

            status = "Overvalued"

        else:

            status = "Fair Value"

        return {

            "model": "Residual Income",

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