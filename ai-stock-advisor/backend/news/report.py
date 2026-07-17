from datetime import datetime


class NewsReport:
    """
    Builds the final News Engine report.
    Standardized format shared across all engines.
    """

    @staticmethod
    def build(

        ticker,

        articles,

        classifications,

        impacts,

        sentiments,

        summary,

        recommendation,

    ):

        return {

            # -------------------------------------------------
            # Engine Metadata
            # -------------------------------------------------

            "engine": "News",

            "version": "1.0",

            "generated_at": datetime.utcnow().isoformat(),

            "ticker": ticker,

            # -------------------------------------------------
            # Analysis
            # -------------------------------------------------

            "analysis": {

                "summary": summary,

                "statistics": {

                    "total_articles": len(articles),

                    "categories": summary.get(
                        "category_distribution",
                        {},
                    ),

                    "sentiments": summary.get(
                        "sentiment_distribution",
                        {},
                    ),

                    "impacts": summary.get(
                        "impact_distribution",
                        {},
                    ),

                },

                "articles": [

                    {

                        **article,

                        "classification": classification,

                        "impact": impact,

                        "sentiment": sentiment,

                    }

                    for article,
                    classification,
                    impact,
                    sentiment

                    in zip(

                        articles,

                        classifications,

                        impacts,

                        sentiments,

                    )

                ]

            },

            # -------------------------------------------------
            # Scores
            # -------------------------------------------------

            "scores": {

                "news_score": recommendation["news_score"],

            },

            # -------------------------------------------------
            # Recommendation
            # -------------------------------------------------

            "recommendation": recommendation,

        }