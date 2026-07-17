class TaxForecast:
    """
    Converts EBIT into NOPAT.
    """

    def forecast(
        self,
        ebit,
        assumptions,
    ):

        tax_rate = assumptions["tax_rate"]

        nopat = []

        for value in ebit:

            nopat.append(

                round(

                    value * (1 - tax_rate),

                    2,

                )

            )

        return nopat