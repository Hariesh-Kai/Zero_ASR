class ComparisonMetrics:
    """
    Extracts comparable metrics from
    all analysis engines.
    """

    @staticmethod
    def extract(

        data,

    ):

        fundamental = data["fundamental"]

        technical = data["technical"]

        news = data["news"]

        valuation = data["valuation"]

        advisor = data["advisor"]

        return {

            "company": fundamental["company"]["name"],

            "ticker": fundamental["company"]["ticker"],

            # ----------------------------------
            # Fundamental
            # ----------------------------------

            "fundamental_score":
                fundamental["scores"]["overall"]["overall_score"],

            "fundamental_recommendation":
                fundamental["recommendation"]["recommendation"],

            # ----------------------------------
            # Technical
            # ----------------------------------

            "technical_score":
                technical["scores"]["technical_score"],

            "technical_recommendation":
                technical["recommendation"]["recommendation"],

            # ----------------------------------
            # News
            # ----------------------------------

            "news_score":
                news["scores"]["news_score"],

            "news_recommendation":
                news["recommendation"]["recommendation"],

            # ----------------------------------
            # Valuation
            # ----------------------------------

            "fair_value":
                valuation["recommendation"]["overall_fair_value"],

            "current_price":
                valuation["valuations"]["dcf"]["company"]["current_price"],

            "upside":
                valuation["valuations"]["dcf"]["valuation"]["upside"],

            "valuation_recommendation":
                valuation["recommendation"]["recommendation"],
                        # ----------------------------------
            # Advisor
            # ----------------------------------

            "advisor_score":
                advisor["advisor_score"],

            "advisor_recommendation":
                advisor["recommendation"]["recommendation"],

        }