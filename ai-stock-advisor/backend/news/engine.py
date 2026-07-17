from news.collector import NewsCollector
from news.analyzer import NewsAnalyzer
from news.deduplicator import NewsDeduplicator
from news.classifier import NewsClassifier
from news.impact import NewsImpactAnalyzer
from news.sentiment import NewsSentimentAnalyzer
from news.summarizer import NewsSummarizer
from news.recommendation import NewsRecommendation
from news.report import NewsReport


class NewsEngine:
    """
    Complete News Analysis Engine.
    """

    def __init__(self):

        self.collector = NewsCollector()

        self.analyzer = NewsAnalyzer()

        self.deduplicator = NewsDeduplicator()

        self.classifier = NewsClassifier()

        self.impact = NewsImpactAnalyzer()

        self.sentiment = NewsSentimentAnalyzer()

        self.summarizer = NewsSummarizer()

        self.recommendation = NewsRecommendation()

        self.report = NewsReport()

    def analyze(
        self,
        ticker: str,
    ):

        # --------------------------------
        # Collect
        # --------------------------------

        raw_articles = self.collector.collect(
            ticker
        )

        # --------------------------------
        # Normalize
        # --------------------------------

        articles = self.analyzer.analyze(
            raw_articles
        )

        # --------------------------------
        # Remove duplicates
        # --------------------------------

        articles = self.deduplicator.deduplicate(
            articles
        )

        # --------------------------------
        # Classify
        # --------------------------------

        classifications = [

            self.classifier.classify(
                article
            )

            for article in articles

        ]

        # --------------------------------
        # Impact
        # --------------------------------

        impacts = [

            self.impact.analyze(
                classification
            )

            for classification in classifications

        ]

        # --------------------------------
        # Sentiment
        # --------------------------------

        sentiments = [

            self.sentiment.analyze(
                article
            )

            for article in articles

        ]

        # --------------------------------
        # Summary
        # --------------------------------

        summary = self.summarizer.summarize(

            articles,

            classifications,

            impacts,

            sentiments,

        )

        # --------------------------------
        # Recommendation
        # --------------------------------

        recommendation = (

            self.recommendation.recommend(

                summary

            )

        )

        # --------------------------------
        # Report
        # --------------------------------

        return self.report.build(

            ticker,

            articles,

            classifications,

            impacts,

            sentiments,

            summary,

            recommendation,

        )

        report["recommendation"] = recommendation

        return report