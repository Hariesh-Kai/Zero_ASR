class RevenueForecast:
    """
    Projects revenue for future years.
    """

    def forecast(

        self,

        revenue,

        assumptions,

    ):

        revenues = []

        current = revenue

        for year in range(

            assumptions["forecast_years"]

        ):

            if year < assumptions["high_growth_years"]:

                growth = assumptions["high_growth_rate"]

            else:

                growth = assumptions["stable_growth_rate"]

            current *= (

                1 + growth

            )

            revenues.append(

                round(current, 2)

            )

        return revenues