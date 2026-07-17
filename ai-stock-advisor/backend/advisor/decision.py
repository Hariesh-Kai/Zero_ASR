class DecisionEngine:
    """
    Converts the Advisor Score into
    a final investment recommendation.
    """

    @staticmethod
    def decide(advisor_score: float):

        if advisor_score >= 90:

            recommendation = "Strong Buy"
            rating = "★★★★★"
            confidence = "Very High"

        elif advisor_score >= 75:

            recommendation = "Buy"
            rating = "★★★★☆"
            confidence = "High"

        elif advisor_score >= 60:

            recommendation = "Hold"
            rating = "★★★☆☆"
            confidence = "Medium"

        elif advisor_score >= 40:

            recommendation = "Sell"
            rating = "★★☆☆☆"
            confidence = "Low"

        else:

            recommendation = "Strong Sell"
            rating = "★☆☆☆☆"
            confidence = "Very Low"

        return {

            "advisor_score": advisor_score,

            "rating": rating,

            "recommendation": recommendation,

            "confidence": confidence,

        }