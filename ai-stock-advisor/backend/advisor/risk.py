class RiskEngine:
    """
    Determines investment risk using the
    Fundamental, Technical and News engines.
    """

    @staticmethod
    def assess(

        fundamental,

        technical,

        news,

        valuation,

    ):

        risk_score = 0

        # --------------------------------
        # Fundamental Risk
        # --------------------------------

        fundamental_score = (
            fundamental["scores"]["overall"]["overall_score"]
        )

        if fundamental_score >= 80:

            risk_score += 10

        elif fundamental_score >= 60:

            risk_score += 20

        else:

            risk_score += 40

        # --------------------------------
        # Technical Risk
        # --------------------------------

        technical_score = (
            technical["scores"]["technical_score"]
        )

        if technical_score >= 80:

            risk_score += 10

        elif technical_score >= 60:

            risk_score += 20

        else:

            risk_score += 40

        # --------------------------------
        # News Risk
        # --------------------------------

        news_score = (
            news["scores"]["news_score"]
        )

        if news_score >= 70:

            risk_score += 10

        elif news_score >= 55:

            risk_score += 20

        else:

            risk_score += 40

        # --------------------------------
        # Valuation Risk
        # --------------------------------

        valuation_confidence = (

            valuation
            .get("recommendation", {})
            .get("confidence", 0)

        )

        if valuation_confidence >= 80:

            risk_score += 10

        elif valuation_confidence >= 60:

            risk_score += 20

        else:

            risk_score += 40
        # --------------------------------
        # Average Risk
        # --------------------------------

        risk_score = round(
            risk_score / 4,
            2,
        )

        # --------------------------------
        # Classification
        # --------------------------------

        if risk_score <= 15:

            level = "Very Low"

        elif risk_score <= 22:

            level = "Low"

        elif risk_score <= 30:

            level = "Medium"

        elif risk_score <= 36:

            level = "High"

        else:

            level = "Very High"

        return {

            "risk_score": risk_score,

            "risk_level": level,

        }