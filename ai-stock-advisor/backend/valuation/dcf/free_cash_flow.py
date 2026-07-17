class FreeCashFlowForecast:
    """
    Calculates future Free Cash Flow.
    """

    def forecast(

        self,

        nopat,

        reinvestment,

    ):

        fcf = []

        for n, r in zip(

            nopat,

            reinvestment,

        ):

            fcf.append(

                round(

                    n - r,

                    2,

                )

            )

        return fcf