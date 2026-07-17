class TerminalValue:
    """
    Calculates the terminal value
    using the Gordon Growth Model.
    """

    def calculate(

        self,

        final_fcf,

        assumptions,

        wacc,

    ):

        g = assumptions["terminal_growth"]

        r = wacc["wacc"]

        terminal_fcf = (

            final_fcf *

            (1 + g)

        )

        terminal_value = (

            terminal_fcf /

            (r - g)

        )

        return {

            "terminal_fcf": round(

                terminal_fcf,

                2,

            ),

            "terminal_value": round(

                terminal_value,

                2,

            ),

        }