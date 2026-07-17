from datetime import datetime


class ComparisonReport:
    """
    Builds the final comparison report.
    """

    @staticmethod
    def build(

        ticker_one,

        ticker_two,

        company_one,

        company_two,

        comparison,

        winner,

        summary,

    ):

        return {

            # ----------------------------------
            # Metadata
            # ----------------------------------

            "engine": "Comparison Engine",

            "version": "1.0",

            "generated_at": datetime.utcnow().isoformat(),

            # ----------------------------------
            # Companies
            # ----------------------------------

            "companies": {

                "left": {

                    "ticker": ticker_one,

                    "name": company_one["company"],

                },

                "right": {

                    "ticker": ticker_two,

                    "name": company_two["company"],

                },

            },

            # ----------------------------------
            # Comparison
            # ----------------------------------

            "comparison": comparison,

            # ----------------------------------
            # Winner
            # ----------------------------------

            "winner": winner,

            # ----------------------------------
            # Summary
            # ----------------------------------

            "summary": summary,

        }