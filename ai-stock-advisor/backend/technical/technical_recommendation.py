class TechnicalRecommendation:
    """
    Converts the technical score into
    an investment recommendation.
    """

    @staticmethod
    def recommend(
        technical_score: float,
    ):

        if technical_score >= 90:

            return {

                "rating": "★★★★★",

                "recommendation": "Strong Buy",

                "confidence": "Very High",
            }

        elif technical_score >= 80:

            return {

                "rating": "★★★★☆",

                "recommendation": "Buy",

                "confidence": "High",
            }

        elif technical_score >= 60:

            return {

                "rating": "★★★☆☆",

                "recommendation": "Hold",

                "confidence": "Medium",
            }

        elif technical_score >= 40:

            return {

                "rating": "★★☆☆☆",

                "recommendation": "Sell",

                "confidence": "Low",
            }

        else:

            return {

                "rating": "★☆☆☆☆",

                "recommendation": "Strong Sell",

                "confidence": "Very Low",
            }