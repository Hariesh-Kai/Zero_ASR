from datetime import datetime


class ValuationReport:
    """
    Builds the final Valuation Engine report.
    """

    def build(

        self,

        ticker,

        results,

        recommendation,

        summary,

    ):

        return {

            # -----------------------------------
            # Engine Metadata
            # -----------------------------------

            "engine": "Valuation",

            "version": "1.0",

            "generated_at": datetime.utcnow().isoformat(),

            "ticker": ticker,

            # -----------------------------------
            # Individual Valuation Models
            # -----------------------------------

            "valuations": results,

            # -----------------------------------
            # Consensus Recommendation
            # -----------------------------------

            "recommendation": recommendation,

            # -----------------------------------
            # AI Summary
            # -----------------------------------

            "summary": summary,

        }