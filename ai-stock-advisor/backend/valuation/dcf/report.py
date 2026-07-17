from datetime import datetime


class DCFReport:
    """
    Builds the complete DCF valuation report.
    """

    @staticmethod
    def build(
        company,
        assumptions,
        revenues,
        ebit,
        nopat,
        reinvestment,
        fcf,
        wacc,
        discounted_fcf,
        terminal,
        discounted_terminal,
        enterprise_value,
        equity,
    ):

        return {

            # ---------------------------------
            # Engine Metadata
            # ---------------------------------

            "engine": "Professional DCF",

            "version": "1.0",

            "generated_at": datetime.utcnow().isoformat(),

            "ticker": company.get("ticker"),

            # ---------------------------------
            # Company
            # ---------------------------------

            "company": company,

            # ---------------------------------
            # Assumptions
            # ---------------------------------

            "assumptions": assumptions,

            # ---------------------------------
            # Forecasts
            # ---------------------------------

            "forecast": {

                "revenue": revenues,

                "ebit": ebit,

                "nopat": nopat,

                "reinvestment": reinvestment,

                "free_cash_flow": fcf,

            },

            # ---------------------------------
            # Discounting
            # ---------------------------------

            "discounting": {

                "wacc": wacc,

                "discounted_fcf": discounted_fcf,

            },

            # ---------------------------------
            # Terminal Value
            # ---------------------------------

            "terminal": {

                **terminal,

                "discounted_terminal": discounted_terminal,

            },

            # ---------------------------------
            # Valuation
            # ---------------------------------

            "valuation": {

                "enterprise_value": enterprise_value,

                **equity,

            },

        }