class VerdictGenerator:
    """
    Generates a final investment verdict
    using strengths, risks, and recommendation.
    """

    def generate(
        self,
        strengths,
        risks,
        recommendation,
    ):

        rating = recommendation.get("recommendation", "Hold")

        intro = {
            "Strong Buy": (
                "The company demonstrates outstanding financial quality "
                "across most evaluation areas."
            ),
            "Buy": (
                "The company shows strong financial fundamentals with "
                "several attractive characteristics."
            ),
            "Hold": (
                "The company has a balanced financial profile with both "
                "strengths and areas that deserve attention."
            ),
            "Sell": (
                "The company exhibits several financial weaknesses that "
                "investors should evaluate carefully."
            ),
            "Strong Sell": (
                "The company's financial profile indicates significant "
                "investment risks."
            ),
        }

        summary = intro.get(
            rating,
            "Financial analysis completed."
        )

        summary += f" Overall recommendation: {rating}."

        return {
            "summary": summary,
            "strength_count": len(strengths),
            "risk_count": len(risks),
        }