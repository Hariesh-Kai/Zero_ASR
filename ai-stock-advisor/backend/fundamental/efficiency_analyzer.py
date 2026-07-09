from fundamental.ratios.efficiency import EfficiencyRatios


class EfficiencyAnalyzer:
    """
    Performs efficiency analysis using mapped financial data.
    """

    def __init__(self):
        self.ratios = EfficiencyRatios()

    def analyze(self, mapped):

        revenue = mapped.get("revenue")
        gross_profit = mapped.get("gross_profit")
        total_assets = mapped.get("total_assets")

        inventory = mapped.get("inventory")
        accounts_receivable = mapped.get("accounts_receivable")

        current_assets = mapped.get("current_assets")
        current_liabilities = mapped.get("current_liabilities")

        # Cost of Revenue = Revenue - Gross Profit
        if revenue is not None and gross_profit is not None:
            cost_of_revenue = revenue - gross_profit
        else:
            cost_of_revenue = None

        asset_turnover = self.ratios.asset_turnover(
            revenue,
            total_assets,
        )

        inventory_turnover = self.ratios.inventory_turnover(
            cost_of_revenue,
            inventory,
        )

        receivables_turnover = self.ratios.receivables_turnover(
            revenue,
            accounts_receivable,
        )

        working_capital_turnover = self.ratios.working_capital_turnover(
            revenue,
            current_assets,
            current_liabilities,
        )

        return {
            "asset_turnover": asset_turnover,
            "inventory_turnover": inventory_turnover,
            "receivables_turnover": receivables_turnover,
            "working_capital_turnover": working_capital_turnover,
        }