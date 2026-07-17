class EVMultipleModel:
    """
    Enterprise Value / EBITDA Valuation.
    """

    def analyze(
        self,
        data,
    ):

        company = data["company"]

        current_price = company.get(
            "current_price"
        )

        enterprise_value = company.get(
            "enterprise_value"
        )

        ebitda = company.get(
            "ebitda"
        )

        shares = company.get(
            "shares_outstanding"
        )

        if not all([

            current_price,

            enterprise_value,

            ebitda,

            shares,

        ]):

            return {

                "model": "EV Multiple",

                "fair_value": None,

                "current_price": current_price,

                "margin_of_safety": None,

                "status": "Unavailable",

            }

        current_multiple = (

            enterprise_value

            /

            ebitda

        )

        fair_multiple = 15

        fair_enterprise = (

            ebitda

            *

            fair_multiple

        )

        fair_value = (

            fair_enterprise

            /

            shares

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

            "model": "EV Multiple",

            "current_multiple": round(
                current_multiple,
                2,
            ),

            "fair_multiple": fair_multiple,

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