from datetime import datetime


class AdvisorReport:
    """
    Builds the final AI Advisor report.
    """

    @staticmethod
    def build(

        ticker,

        weighting,

        decision,

        confidence,

        risk,

        summary,

        fundamental,

        technical,

        news,

        valuation,

    ):

        return {

            # -------------------------------------
            # Metadata
            # -------------------------------------

            "engine": "AI Advisor",

            "version": "1.0",

            "generated_at": datetime.utcnow().isoformat(),

            "ticker": ticker,

            # -------------------------------------
            # Final Decision
            # -------------------------------------

            "advisor_score": weighting["advisor_score"],

            "recommendation": decision,

            "confidence": confidence,

            "risk": risk,

            "summary": summary,

            # -------------------------------------
            # Engine Weighting
            # -------------------------------------

            "weighting": weighting,

            # -------------------------------------
            # Individual Engine Reports
            # -------------------------------------

            "engines": {

                "fundamental": fundamental,

                "technical": technical,

                "news": news,

                "valuation": valuation,

            }

        }