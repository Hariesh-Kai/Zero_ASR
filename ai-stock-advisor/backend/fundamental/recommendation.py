class RecommendationEngine:
    """
    Converts the overall score into an investment recommendation.
    Uses the same thresholds as OverallScore.
    """

    @staticmethod
    def recommend(overall_score: float):

        if overall_score >= 90:
            return {
                "rating": "★★★★★",
                "recommendation": "Strong Buy",
                "confidence": "Very High"
            }

        elif overall_score >= 75:
            return {
                "rating": "★★★★☆",
                "recommendation": "Buy",
                "confidence": "High"
            }

        elif overall_score >= 60:
            return {
                "rating": "★★★☆☆",
                "recommendation": "Hold",
                "confidence": "Medium"
            }

        elif overall_score >= 40:
            return {
                "rating": "★★☆☆☆",
                "recommendation": "Sell",
                "confidence": "Low"
            }

        else:
            return {
                "rating": "★☆☆☆☆",
                "recommendation": "Strong Sell",
                "confidence": "Very Low"
            }