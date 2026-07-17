class NewsRecommendation:
    """
    Generates an investment recommendation
    from the news summary.
    """

    def recommend(self, summary):

        sentiment = summary["overall_sentiment"]
        impact = summary["overall_impact"]

        score = 50

        # --------------------------
        # Sentiment
        # --------------------------

        if sentiment == "Positive":
            score += 25

        elif sentiment == "Negative":
            score -= 25

        # --------------------------
        # Impact
        # --------------------------

        if impact == "Very High":
            score += 20

        elif impact == "High":
            score += 10

        elif impact == "Medium":
            score += 5

        score = max(0, min(score, 100))

        # --------------------------
        # Recommendation
        # --------------------------

        if score >= 85:

            recommendation = "Strong Bullish"

            rating = "★★★★★"

            confidence = "Very High"

        elif score >= 70:

            recommendation = "Bullish"

            rating = "★★★★☆"

            confidence = "High"

        elif score >= 55:

            recommendation = "Neutral"

            rating = "★★★☆☆"

            confidence = "Medium"

        elif score >= 40:

            recommendation = "Bearish"

            rating = "★★☆☆☆"

            confidence = "Medium"

        else:

            recommendation = "Strong Bearish"

            rating = "★☆☆☆☆"

            confidence = "High"

        return {

            "news_score": score,

            "rating": rating,

            "recommendation": recommendation,

            "confidence": confidence,

        }