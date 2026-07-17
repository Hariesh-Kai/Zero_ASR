class ComparisonWinner:
    """
    Determines the overall winner
    of the comparison.
    """

    @staticmethod
    def decide(

        scoreboard,

    ):

        tickers = list(

            scoreboard.keys()

        )

        ticker_one = tickers[0]

        ticker_two = tickers[1]

        score_one = scoreboard[

            ticker_one

        ]

        score_two = scoreboard[

            ticker_two

        ]

        # ----------------------------------
        # Decide Winner
        # ----------------------------------

        if score_one > score_two:

            winner = ticker_one

            margin = score_one - score_two

            result = "Winner"

        elif score_two > score_one:

            winner = ticker_two

            margin = score_two - score_one

            result = "Winner"

        else:

            winner = "Tie"

            margin = 0

            result = "Draw"

        # ----------------------------------
        # Return
        # ----------------------------------

        return {

            "winner": winner,

            "result": result,

            "margin": margin,

            "scoreboard": scoreboard,

        }