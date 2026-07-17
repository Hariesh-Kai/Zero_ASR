class NewsClassifier:
    """
    Classifies a news article into a financial event category.
    """

    CATEGORIES = {

        "Earnings": [
            "earnings",
            "quarterly",
            "results",
            "revenue",
            "profit",
            "eps",
            "guidance",
            "forecast",
        ],

        "Merger & Acquisition": [
            "acquire",
            "acquires",
            "acquisition",
            "merge",
            "merger",
            "takeover",
        ],

        "Executive Change": [
            "ceo",
            "cfo",
            "chairman",
            "executive",
            "resigns",
            "appointed",
        ],

        "Dividend": [
            "dividend",
            "buyback",
            "share repurchase",
        ],

        "Product Launch": [
            "launch",
            "introduces",
            "announces",
            "release",
            "product",
        ],

        "AI": [
            "artificial intelligence",
            "ai",
            "chatgpt",
            "copilot",
            "openai",
            "llm",
        ],

        "Chip": [
            "chip",
            "gpu",
            "cpu",
            "semiconductor",
            "nvidia",
            "amd",
            "intel",
        ],

        "Partnership": [
            "partnership",
            "collaboration",
            "agreement",
            "joint venture",
        ],

        "Lawsuit": [
            "lawsuit",
            "court",
            "legal",
            "sec",
            "investigation",
            "fine",
        ],

        "Macro Economy": [
            "inflation",
            "interest rate",
            "federal reserve",
            "fed",
            "recession",
            "economy",
        ],

    }

    def classify(self, article):

        text = " ".join([
            article.get("title", ""),
            article.get("description", ""),
            article.get("summary", ""),
        ]).lower()

        for category, keywords in self.CATEGORIES.items():

            for keyword in keywords:

                if keyword in text:

                    return {
                        "category": category,
                        "matched_keyword": keyword,
                    }

        return {
            "category": "General",
            "matched_keyword": None,
        }