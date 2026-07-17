class OperatingMarginForecast:
    """
    Forecasts EBIT using a target operating margin.
    """

    def forecast(
        self,
        revenues,
        assumptions,
    ):

        margin = assumptions["target_operating_margin"]

        ebit = []

        for revenue in revenues:

            ebit.append(

                round(

                    revenue * margin,

                    2,

                )

            )

        return ebit