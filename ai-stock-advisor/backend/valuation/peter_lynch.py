class PeterLynchModel:
    """
    Peter Lynch Fair Value Model.
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

        growth = company.get(
            "earnings_growth"
        )

        if not all([

            current_price,

            eps,

            growth,

        ]):

            return {

                "model": "Peter Lynch",

                "fair_value": None,

                "current_price": current_price,

                "margin_of_safety": None,

                "status": "Unavailable",

            }

        # Convert growth from decimal to percentage

        growth_percent = growth * 100

        fair_pe = growth_percent

        fair_value = eps * fair_pe

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

            "model": "Peter Lynch",

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