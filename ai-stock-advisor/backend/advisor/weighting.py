class WeightingEngine:
    """
    Combines the scores from all analysis engines
    into one Advisor Score.

    Current Strategy:
        Fundamental : 45%
        Technical   : 35%
        News        : 20%

    Future versions can make these
    weights dynamic based on the
    investment strategy.
    """

    FUNDAMENTAL_WEIGHT = 0.35

    VALUATION_WEIGHT = 0.30

    TECHNICAL_WEIGHT = 0.20

    NEWS_WEIGHT = 0.15

    @classmethod
    def calculate(

        cls,

        fundamental,

        technical,

        news,

        valuation,

    ):

        # -----------------------------
        # Extract Scores
        # -----------------------------

        fundamental_score = (
            fundamental["scores"]["overall"]["overall_score"]
        )

        technical_score = (
            technical["scores"]["technical_score"]
        )

        news_score = (
            news["scores"]["news_score"]
        )

        valuation_score = (
            valuation
            .get("recommendation", {})
            .get("confidence", 0)
        )

        # -----------------------------
        # Weighted Score
        # -----------------------------

        advisor_score = round(

            (

                fundamental_score
                * cls.FUNDAMENTAL_WEIGHT

                +

                valuation_score
                * cls.VALUATION_WEIGHT

                +

                technical_score
                * cls.TECHNICAL_WEIGHT

                +

                news_score
                * cls.NEWS_WEIGHT

            ),

            2,

        )

        # -----------------------------
        # Return
        # -----------------------------

        return {

            "fundamental": {

                "score": fundamental_score,

                "weight": cls.FUNDAMENTAL_WEIGHT,

                "weighted_score": round(
                    fundamental_score
                    * cls.FUNDAMENTAL_WEIGHT,
                    2,
                ),

            },

            "valuation": {

            "score": valuation_score,

            "weight": cls.VALUATION_WEIGHT,

            "weighted_score": round(

                valuation_score
                * cls.VALUATION_WEIGHT,

                2,

            ),

        },

            "technical": {

                "score": technical_score,

                "weight": cls.TECHNICAL_WEIGHT,

                "weighted_score": round(
                    technical_score
                    * cls.TECHNICAL_WEIGHT,
                    2,
                ),

            },

            "news": {

                "score": news_score,

                "weight": cls.NEWS_WEIGHT,

                "weighted_score": round(
                    news_score
                    * cls.NEWS_WEIGHT,
                    2,
                ),

            },

            "advisor_score": advisor_score,

        }