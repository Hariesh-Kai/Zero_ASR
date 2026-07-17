class ComparisonSummary:
    """
    Generates a human-readable summary
    of the comparison.
    """

    @staticmethod
    def generate(

        company_one,

        company_two,

        comparison,

        winner,

    ):

        ticker_one = company_one["ticker"]

        ticker_two = company_two["ticker"]

        score_one = winner["scoreboard"][

            ticker_one

        ]

        score_two = winner["scoreboard"][

            ticker_two

        ]

        # ----------------------------------
        # Summary
        # ----------------------------------

        if winner["winner"] == "Tie":

            return (

                f"{ticker_one} and {ticker_two} "

                f"performed equally across the "

                f"comparison metrics. "

                f"Both companies achieved "

                f"{score_one} points, "

                f"making this a balanced "

                f"investment comparison."

            )

        return (

            f"{winner['winner']} is the stronger "

            f"investment based on the current "

            f"analysis. "

            f"It won "

            f"{winner['margin']} "

            f"more comparison categories "

            f"than its competitor "

            f"({score_one} vs {score_two}). "

            f"The comparison considered "

            f"Fundamental Analysis, "

            f"Technical Analysis, "

            f"News Sentiment, "

            f"Valuation and "

            f"AI Advisor Score."

        )