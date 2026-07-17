class ReinvestmentForecast:
    """
    Estimates reinvestment required to support
    future revenue growth.
    """

    def forecast(
        self,
        revenues,
        current_revenue,
        assumptions,
    ):

        ratio = assumptions["sales_to_capital"]

        reinvestment = []

        previous = current_revenue

        for revenue in revenues:

            increase = revenue - previous

            reinvestment.append(

                round(

                    increase / ratio,

                    2,

                )

            )

            previous = revenue

        return reinvestment