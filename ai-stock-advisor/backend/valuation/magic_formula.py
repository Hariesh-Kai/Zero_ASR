class MagicFormulaModel:
    """
    Joel Greenblatt Magic Formula.
    """

    def analyze(
        self,
        data,
    ):

        company = data["company"]

        current_price = company.get(
            "current_price"
        )

        ebit = company.get(
            "ebitda"
        )

        enterprise_value = company.get(
            "enterprise_value"
        )

        if not all([

            current_price,

            ebit,

            enterprise_value,

        ]):

            return {

                "model": "Magic Formula",

                "earnings_yield": None,

                "return_on_capital": None,

                "score": None,

                "status": "Unavailable",

            }

        earnings_yield = (

            ebit

            /

            enterprise_value

        ) * 100

        roc = (

            company.get(
                "return_on_equity",
                0,
            )

        ) * 100

        score = (

            earnings_yield

            +

            roc

        ) / 2

        if score >= 20:

            status = "Excellent"

        elif score >= 12:

            status = "Good"

        elif score >= 8:

            status = "Average"

        else:

            status = "Poor"

        return {

            "model": "Magic Formula",

            "earnings_yield": round(
                earnings_yield,
                2,
            ),

            "return_on_capital": round(
                roc,
                2,
            ),

            "score": round(
                score,
                2,
            ),

            "status": status,

        }