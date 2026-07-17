class ValuationRecommendation:
    """
    Combines all valuation models into one recommendation.
    """

    def recommend(
        self,
        valuations,
    ):

        fair_values = []

        statuses = []

        weights = {

            "dcf": 3,

            "owner_earnings": 2,

            "graham": 2,

            "peter_lynch": 1,

            "ev_multiple": 1,

            "residual_income": 1,

        }

        weighted_sum = 0

        total_weight = 0

        for name, model in valuations.items():

            fair_value = model.get("fair_value")

            status = model.get("status")

            if fair_value is not None:

                weight = weights.get(

                    name,

                    1,

                )

                weighted_sum += (

                    fair_value *

                    weight

                )

                total_weight += weight

            if status:

                statuses.append(

                    status

                )

        if total_weight == 0:

            return {

                "overall_fair_value": None,

                "recommendation": "Unavailable",

                "confidence": 0,

                "agreement": "0/0",

            }

        overall = (

            weighted_sum /

            total_weight

        )

        over = statuses.count(

            "Overvalued"

        )

        under = statuses.count(

            "Undervalued"

        )

        fair = statuses.count(

            "Fair Value"

        )

        total = len(statuses)

        winner = max(

            over,

            under,

            fair,

        )

        confidence = round(

            winner /

            total *

            100,

            1,

        )

        if under > over and under > fair:

            recommendation = "Undervalued"

            agreement = f"{under}/{total}"

        elif over > under and over > fair:

            recommendation = "Overvalued"

            agreement = f"{over}/{total}"

        else:

            recommendation = "Fair Value"

            agreement = f"{fair}/{total}"

        return {

            "overall_fair_value": round(

                overall,

                2,

            ),

            "recommendation": recommendation,

            "confidence": confidence,

            "agreement": agreement,

        }