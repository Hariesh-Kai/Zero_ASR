class TechnicalScoring:
    """
    Combines all analyzer scores into one
    weighted technical score out of 100.
    """

    TREND_WEIGHT = 0.40
    MOMENTUM_WEIGHT = 0.25
    VOLUME_WEIGHT = 0.20
    VOLATILITY_WEIGHT = 0.15

    @staticmethod
    def score(results):

        trend = results["trend"]
        momentum = results["momentum"]
        volume = results["volume"]
        volatility = results["volatility"]

        # Trend Analyzer V2
        trend_score = trend["trend_score"]

        # Remaining analyzers are still V1
        momentum_score = (
            momentum["score"] / momentum["max_score"]
        ) * 100

        volume_score = (
            volume["score"] / volume["max_score"]
        ) * 100

        volatility_score = (
            volatility["score"] / volatility["max_score"]
        ) * 100

        technical_score = round(

            (
                trend_score * TechnicalScoring.TREND_WEIGHT
                + momentum_score * TechnicalScoring.MOMENTUM_WEIGHT
                + volume_score * TechnicalScoring.VOLUME_WEIGHT
                + volatility_score * TechnicalScoring.VOLATILITY_WEIGHT
            ),

            2,

        )

        if technical_score >= 90:

            grade = "A+"

        elif technical_score >= 80:

            grade = "A"

        elif technical_score >= 70:

            grade = "B"

        elif technical_score >= 60:

            grade = "C"

        elif technical_score >= 50:

            grade = "D"

        else:

            grade = "F"

        return {

            "trend": round(trend_score, 2),

            "momentum": round(momentum_score, 2),

            "volume": round(volume_score, 2),

            "volatility": round(volatility_score, 2),

            "technical_score": technical_score,

            "grade": grade,
        }