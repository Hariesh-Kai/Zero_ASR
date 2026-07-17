class DiscountCashFlow:
    """
    Discounts future Free Cash Flows
    to present value.
    """

    def discount(
        self,
        fcf,
        wacc,
    ):

        discounted = []

        rate = wacc["wacc"]

        for year, cashflow in enumerate(

            fcf,

            start=1,

        ):

            pv = cashflow / (

                (1 + rate) ** year

            )

            discounted.append(

                round(

                    pv,

                    2,

                )

            )

        return discounted