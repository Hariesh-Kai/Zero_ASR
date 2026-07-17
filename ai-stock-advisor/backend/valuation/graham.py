class GrahamModel:
    """
    Benjamin Graham Intrinsic Value Model.
    """

    def analyze(
        self,
        data,
    ):

        company = data["company"]

        current_price = company.get(
            "current_price"
        )

        eps = company.get(
            "eps"
        )

        if not all([

            current_price,

            eps,

        ]):

            return {

                "model": "Graham",

                "fair_value": None,

                "current_price": current_price,

                "margin_of_safety": None,

                "status": "Unavailable",

            }

        # ------------------------------------
        # Graham Formula
        # ------------------------------------

        bond_yield = 4.4

        fair_value = (

            eps *

            (8.5 + 2 * 10)

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

            "model": "Graham",

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