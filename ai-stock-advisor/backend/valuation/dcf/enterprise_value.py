class EnterpriseValue:
    """
    Calculates Enterprise Value.
    """

    def calculate(

        self,

        discounted_fcf,

        discounted_terminal,

    ):

        return round(

            sum(

                discounted_fcf

            ) + discounted_terminal,

            2,

        )