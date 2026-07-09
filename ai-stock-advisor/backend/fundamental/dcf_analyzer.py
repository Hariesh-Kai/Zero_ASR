class DCFAnalyzer:
    """
    Discounted Cash Flow (DCF) Intrinsic Valuation.

    Estimates intrinsic enterprise value using
    Free Cash Flow growth.
    """

    @staticmethod
    def _safe(value):
        return 0 if value is None else value

    def analyze(
        self,
        mapped,
        growth,
    ):

        free_cash_flow = self._safe(
            mapped.get("free_cash_flow")
        )

        cashflow_growth = growth.get(
            "cashflow_growth"
        )

        if cashflow_growth is None:
            cashflow_growth = 5

        # -----------------------------------
        # Assumptions
        # -----------------------------------

        growth_rate = min(
            max(cashflow_growth / 100, 0.02),
            0.20,
        )

        discount_rate = 0.10
        terminal_growth = 0.03

        cashflows = []

        fcf = free_cash_flow

        # Forecast next 5 years
        for _ in range(5):

            fcf *= (1 + growth_rate)

            discounted = fcf / (
                (1 + discount_rate)
                ** (_ + 1)
            )

            cashflows.append(discounted)

        terminal_value = (

            fcf
            * (1 + terminal_growth)

        ) / (

            discount_rate
            - terminal_growth

        )

        terminal_value /= (

            (1 + discount_rate)
            ** 5

        )

        intrinsic_value = (
            sum(cashflows)
            + terminal_value
        )

        market_cap = mapped.get(
            "market_cap"
        )

        current_price = mapped.get(
            "current_price"
        )

        if market_cap:

            if intrinsic_value > market_cap:
                verdict = "Undervalued"

            elif intrinsic_value < market_cap:
                verdict = "Overvalued"

            else:
                verdict = "Fairly Valued"

        else:

            verdict = "Unknown"

        margin_of_safety = None

        if (
            current_price is not None
            and market_cap
            and market_cap > 0
        ):

            shares_outstanding = market_cap / current_price

            intrinsic_price = intrinsic_value / shares_outstanding

            margin_of_safety = (
                (intrinsic_price - current_price)
                / current_price
            ) * 100

        return {

            "intrinsic_value": intrinsic_value,

            "current_price": current_price,

            "margin_of_safety": margin_of_safety,

            "market_cap": market_cap,

            "growth_rate": growth_rate * 100,

            "discount_rate": discount_rate * 100,

            "terminal_growth_rate": terminal_growth * 100,

            "valuation": verdict,
        }