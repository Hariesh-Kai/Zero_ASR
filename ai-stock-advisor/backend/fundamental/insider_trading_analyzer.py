class InsiderTradingAnalyzer:
    """
    Evaluates recent insider buying/selling
    activity.
    """

    @staticmethod
    def _safe(value):
        return 0 if value is None else value

    def analyze(
        self,
        company_info,
    ):

        net_percent = self._safe(
            company_info.get("heldPercentInsiders")
        )

        net_percent *= 100

        score = 3

        if net_percent >= 20:
            score = 5

        elif net_percent >= 10:
            score = 4

        elif net_percent >= 5:
            score = 3

        elif net_percent >= 1:
            score = 2

        else:
            score = 1

        if score == 5:
            sentiment = "Strong Buying"

        elif score == 4:
            sentiment = "Buying"

        elif score == 3:
            sentiment = "Neutral"

        elif score == 2:
            sentiment = "Selling"

        else:
            sentiment = "Strong Selling"

        return {
            "score": score,
            "max_score": 5,
            "insider_percent": net_percent,
            "sentiment": sentiment,
        }