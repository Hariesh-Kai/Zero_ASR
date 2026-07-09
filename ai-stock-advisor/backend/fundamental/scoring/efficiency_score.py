class EfficiencyScore:
    """
    Scores operational efficiency.
    Maximum Score: 100
    """

    @staticmethod
    def score(
        asset_turnover,
        inventory_turnover,
        receivables_turnover,
        working_capital_turnover,
    ):

        score = 0

        # Asset Turnover (25)
        if asset_turnover is not None:
            if asset_turnover >= 1.0:
                score += 25
            elif asset_turnover >= 0.75:
                score += 20
            elif asset_turnover >= 0.50:
                score += 15
            elif asset_turnover >= 0.25:
                score += 10

        # Inventory Turnover (25)
        if inventory_turnover is not None:
            if inventory_turnover >= 8:
                score += 25
            elif inventory_turnover >= 6:
                score += 20
            elif inventory_turnover >= 4:
                score += 15
            elif inventory_turnover >= 2:
                score += 10

        # Receivables Turnover (25)
        if receivables_turnover is not None:
            if receivables_turnover >= 10:
                score += 25
            elif receivables_turnover >= 8:
                score += 20
            elif receivables_turnover >= 6:
                score += 15
            elif receivables_turnover >= 4:
                score += 10

        # Working Capital Turnover (25)
        if working_capital_turnover is not None:
            if working_capital_turnover >= 5:
                score += 25
            elif working_capital_turnover >= 4:
                score += 20
            elif working_capital_turnover >= 3:
                score += 15
            elif working_capital_turnover >= 2:
                score += 10

        return score