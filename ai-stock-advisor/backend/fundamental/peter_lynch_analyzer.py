class PeterLynchAnalyzer:
    """
    Peter Lynch Fair Value Model.

    Fair P/E = EPS Growth (%)

    Fair Price = EPS × Fair P/E
    """

    @staticmethod
    def analyze(
        company,
        growth,
    ):

        current_price = company.get(
            "current_price"
        )

        eps = company.get(
            "eps"
        )

        eps_growth = growth.get(
            "eps_growth"
        )

        if (
            current_price is None
            or eps is None
            or eps_growth is None
        ):
            return {
                "fair_pe": None,
                "fair_price": None,
                "current_price": current_price,
                "upside": None,
                "valuation": "Unknown",
            }

        fair_pe = eps_growth

        fair_price = eps * fair_pe

        upside = (
            (fair_price - current_price)
            / current_price
        ) * 100

        if upside >= 20:
            valuation = "Undervalued"

        elif upside <= -20:
            valuation = "Overvalued"

        else:
            valuation = "Fairly Valued"

        return {

            "fair_pe": fair_pe,

            "fair_price": fair_price,

            "current_price": current_price,

            "upside": upside,

            "valuation": valuation,
        }