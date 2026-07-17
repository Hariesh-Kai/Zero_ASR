class ValuationSummary:
    """
    Generates a human-readable valuation summary.
    """

    def generate(
        self,
        results,
    ):

        recommendation = results["recommendation"]

        if recommendation["overall_fair_value"] is None:

            return (

                "There is insufficient financial data "

                "to estimate the intrinsic value "

                "of this company."

            )

        return (

            f"The estimated intrinsic value of the stock is "

            f"${recommendation['overall_fair_value']:.2f}. "

            f"Based on the combined valuation models, "

            f"the stock appears "

            f"{recommendation['recommendation'].lower()}. "

            f"{recommendation['agreement']} valuation models "

            f"agree with this conclusion, "

            f"giving an overall confidence of "

            f"{recommendation['confidence']}%."

        )