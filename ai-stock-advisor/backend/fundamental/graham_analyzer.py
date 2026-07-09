class GrahamAnalyzer:
    """
    Benjamin Graham Intrinsic Value Analysis.

    Formula:
    Intrinsic Value = EPS × (8.5 + 2 × Growth Rate)
    """

    @staticmethod
    def _safe(value):
        return 0 if value is None else value

    def analyze(self, mapped, growth):

        eps = self._safe(
            mapped.get("eps")
        )

        eps_growth = growth.get(
            "eps_growth"
        )

        if eps_growth is None:
            eps_growth = 0

        current_price = mapped.get(
            "current_price"
        )

        intrinsic_value = (
            eps
            * (
                8.5
                + (2 * eps_growth)
            )
        )

        upside = None

        if (
            current_price is not None
            and current_price > 0
        ):

            upside = (
                (intrinsic_value - current_price)
                / current_price
            ) * 100

        if current_price is None:
            valuation = "Unknown"

        elif intrinsic_value > current_price:
            valuation = "Undervalued"

        elif intrinsic_value < current_price:
            valuation = "Overvalued"

        else:
            valuation = "Fairly Valued"

        return {
            "intrinsic_value": intrinsic_value,
            "current_price": current_price,
            "upside": upside,
            "valuation": valuation,
        }