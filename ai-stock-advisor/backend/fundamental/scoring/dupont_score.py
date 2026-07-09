class DupontScore:
    """
    Scores the DuPont Analysis (0-100).

    Components:
    - Net Profit Margin
    - Asset Turnover
    - Equity Multiplier
    - ROE
    """

    @staticmethod
    def score(
        net_profit_margin,
        asset_turnover,
        equity_multiplier,
        roe,
    ):

        score = 0

        # ----------------------------------
        # Net Profit Margin (25)
        # ----------------------------------

        if net_profit_margin is not None:

            if net_profit_margin >= 20:
                score += 25

            elif net_profit_margin >= 15:
                score += 20

            elif net_profit_margin >= 10:
                score += 15

            elif net_profit_margin >= 5:
                score += 10

        # ----------------------------------
        # Asset Turnover (25)
        # ----------------------------------

        if asset_turnover is not None:

            if asset_turnover >= 1.0:
                score += 25

            elif asset_turnover >= 0.75:
                score += 20

            elif asset_turnover >= 0.50:
                score += 15

            elif asset_turnover >= 0.25:
                score += 10

        # ----------------------------------
        # Equity Multiplier (25)
        # Lower is generally better
        # ----------------------------------

        if equity_multiplier is not None:

            if equity_multiplier <= 2:
                score += 25

            elif equity_multiplier <= 3:
                score += 20

            elif equity_multiplier <= 4:
                score += 15

            elif equity_multiplier <= 5:
                score += 10

        # ----------------------------------
        # ROE (25)
        # ----------------------------------

        if roe is not None:

            if roe >= 25:
                score += 25

            elif roe >= 20:
                score += 20

            elif roe >= 15:
                score += 15

            elif roe >= 10:
                score += 10

        return score