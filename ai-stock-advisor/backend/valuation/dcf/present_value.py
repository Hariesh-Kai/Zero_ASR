class PresentValue:
    """
    Calculates the present value of the terminal value.
    """

    def calculate(
        self,
        terminal,
        assumptions,
        wacc,
    ):

        years = assumptions["forecast_years"]

        rate = wacc["wacc"]

        pv = terminal["terminal_value"] / (

            (1 + rate) ** years

        )

        return round(

            pv,

            2,

        )