from transformers import pipeline


class NewsSentimentAnalyzer:
    """
    Financial sentiment analysis using FinBERT.
    """

    def __init__(self):

        self.model = pipeline(
            "text-classification",
            model="ProsusAI/finbert"
        )

    def analyze(self, article):

        text = " ".join([
            article.get("title", ""),
            article.get("description", ""),
            article.get("summary", ""),
        ])

        result = self.model(text)[0]

        label = result["label"].capitalize()
        score = round(result["score"] * 100, 2)

        return {

            "sentiment": label,

            "confidence": score,

            "model": "FinBERT",

            "raw": result,
        }