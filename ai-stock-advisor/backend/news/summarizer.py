from collections import Counter


class NewsSummarizer:
    """
    Creates a concise summary from classified news.
    """

    def summarize(
        self,
        articles,
        classifications,
        impacts,
        sentiments,
    ):

        total_articles = len(articles)

        category_counts = Counter(
            item["category"]
            for item in classifications
        )

        sentiment_counts = Counter(
            item["sentiment"]
            for item in sentiments
        )

        impact_counts = Counter(
            item["impact"]
            for item in impacts
        )

        top_category = (
            category_counts.most_common(1)[0][0]
            if category_counts
            else "General"
        )

        overall_sentiment = (
            sentiment_counts.most_common(1)[0][0]
            if sentiment_counts
            else "Neutral"
        )

        overall_impact = (
            impact_counts.most_common(1)[0][0]
            if impact_counts
            else "Low"
        )

        return {

            "total_articles": total_articles,

            "dominant_category": top_category,

            "overall_sentiment": overall_sentiment,

            "overall_impact": overall_impact,

            "category_distribution": dict(category_counts),

            "sentiment_distribution": dict(sentiment_counts),

            "impact_distribution": dict(impact_counts),

            "summary": (
                f"Analyzed {total_articles} news articles. "
                f"Most articles were related to {top_category}. "
                f"Overall sentiment is {overall_sentiment}. "
                f"Overall impact is {overall_impact}."
            ),
        }