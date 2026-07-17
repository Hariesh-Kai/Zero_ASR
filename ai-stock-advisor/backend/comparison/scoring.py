class ComparisonScoring:
    """
    Scores two companies across
    all analysis engines.
    """

    @staticmethod
    def compare(

        company_one,

        company_two,

    ):

        score_one = 0

        score_two = 0

        comparison = {}

        # -----------------------------------
        # Fundamental
        # -----------------------------------

        if (

            company_one["fundamental_score"]

            >

            company_two["fundamental_score"]

        ):

            winner = company_one["ticker"]

            score_one += 1

        elif (

            company_two["fundamental_score"]

            >

            company_one["fundamental_score"]

        ):

            winner = company_two["ticker"]

            score_two += 1

        else:

            winner = "Tie"

        comparison["fundamental"] = {

            "winner": winner,

            company_one["ticker"]:
                company_one["fundamental_score"],

            company_two["ticker"]:
                company_two["fundamental_score"],

        }

        # -----------------------------------
        # Technical
        # -----------------------------------

        if (

            company_one["technical_score"]

            >

            company_two["technical_score"]

        ):

            winner = company_one["ticker"]

            score_one += 1

        elif (

            company_two["technical_score"]

            >

            company_one["technical_score"]

        ):

            winner = company_two["ticker"]

            score_two += 1

        else:

            winner = "Tie"

        comparison["technical"] = {

            "winner": winner,

            company_one["ticker"]:
                company_one["technical_score"],

            company_two["ticker"]:
                company_two["technical_score"],

        }

        # -----------------------------------
        # News
        # -----------------------------------

        if (

            company_one["news_score"]

            >

            company_two["news_score"]

        ):

            winner = company_one["ticker"]

            score_one += 1

        elif (

            company_two["news_score"]

            >

            company_one["news_score"]

        ):

            winner = company_two["ticker"]

            score_two += 1

        else:

            winner = "Tie"

        comparison["news"] = {

            "winner": winner,

            company_one["ticker"]:
                company_one["news_score"],

            company_two["ticker"]:
                company_two["news_score"],

        }

        # -----------------------------------
        # Advisor
        # -----------------------------------

        if (

            company_one["advisor_score"]

            >

            company_two["advisor_score"]

        ):

            winner = company_one["ticker"]

            score_one += 1

        elif (

            company_two["advisor_score"]

            >

            company_one["advisor_score"]

        ):

            winner = company_two["ticker"]

            score_two += 1

        else:

            winner = "Tie"

        comparison["advisor"] = {

            "winner": winner,

            company_one["ticker"]:
                company_one["advisor_score"],

            company_two["ticker"]:
                company_two["advisor_score"],

        }

        # -----------------------------------
        # Valuation
        # Compare DCF Upside
        # -----------------------------------

        upside_one = company_one.get(

            "upside",

            0,

        )

        upside_two = company_two.get(

            "upside",

            0,

        )

        if upside_one > upside_two:

            winner = company_one["ticker"]

            score_one += 1

        elif upside_two > upside_one:

            winner = company_two["ticker"]

            score_two += 1

        else:

            winner = "Tie"

        comparison["valuation"] = {

            "winner": winner,

            company_one["ticker"]:
                round(

                    upside_one,

                    2,

                ),

            company_two["ticker"]:
                round(

                    upside_two,

                    2,

                ),

        }

        return {

            "comparison": comparison,

            "scoreboard": {

                company_one["ticker"]: score_one,

                company_two["ticker"]: score_two,

            },

        }