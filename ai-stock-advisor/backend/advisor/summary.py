class AdvisorSummary:
    """
    Generates a human-readable AI summary.
    """

    @staticmethod
    def generate(
        company: str,
        advisor_score: float,
        recommendation: dict,
        fundamental: dict,
        technical: dict,
        news: dict,
        valuation: dict,
        risk: dict,
    ):

        fundamental_score = (
            fundamental["scores"]["overall"]["overall_score"]
        )

        technical_score = (
            technical["scores"]["technical_score"]
        )

        news_recommendation = (
            news["recommendation"]["recommendation"]
        )

        valuation_recommendation = (
            valuation["recommendation"]["recommendation"]
        )

        fair_value = (
            valuation["recommendation"].get(
                "overall_fair_value"
            )
        )

        if fair_value is None:

            valuation_text = (
                "The valuation engine could not determine "
                "an intrinsic value."
            )

        else:

            valuation_text = (

                f"The valuation engine indicates the stock is "

                f"{valuation_recommendation.lower()} "

                f"with an estimated intrinsic value of "

                f"${fair_value:.2f}."

            )

        return (

            f"{company} has an overall "

            f"{recommendation['recommendation']} "

            f"rating with an AI Advisor score of "

            f"{advisor_score:.2f}/100. "

            f"Fundamental analysis scored "

            f"{fundamental_score:.2f}/100, "

            f"while Technical analysis scored "

            f"{technical_score:.2f}/100. "

            f"Recent news sentiment is "

            f"{news_recommendation}. "

            f"{valuation_text} "

            f"The overall investment risk is "

            f"{risk['risk_level']}."

        )