class ConfidenceEngine:
    """
    Calculates confidence based on how much
    the three engines agree.
    """

    SCALE = {

        "Strong Buy": 5,
        "Buy": 4,
        "Hold": 3,
        "Neutral": 3,
        "Sell": 2,
        "Bearish": 2,
        "Strong Sell": 1,
        "Strong Bearish": 1,

        "Undervalued": 5,
        "Fair Value": 3,
        "Overvalued": 1,

    }

    @classmethod
    def calculate(

        cls,

        fundamental,

        technical,

        news,

        valuation,

    ):

        values = [

            cls.SCALE.get(
                fundamental["recommendation"]["recommendation"],
                3,
            ),

            cls.SCALE.get(
                technical["recommendation"]["recommendation"],
                3,
            ),

            cls.SCALE.get(
                news["recommendation"]["recommendation"],
                3,
            ),

            cls.SCALE.get(
                valuation["recommendation"]["recommendation"],
                3,
            ),

        ]

        average = sum(values) / len(values)

        deviation = sum(

            abs(v - average)

            for v in values

        ) / len(values)

        confidence = round(

            max(

                0,

                100 - deviation * 40,

            ),

            2,

        )

        if confidence >= 90:

            level = "Very High"

        elif confidence >= 75:

            level = "High"

        elif confidence >= 60:

            level = "Medium"

        elif confidence >= 40:

            level = "Low"

        else:

            level = "Very Low"

        return {

            "confidence_score": confidence,

            "confidence": level,

            "engine_scores": values,

            "agreement": f"{sum(v == round(average) for v in values)}/{len(values)}",

        }