from fundamental.ratios.profitability import ProfitabilityRatios
from fundamental.ratios.liquidity import LiquidityRatios
from fundamental.ratios.leverage import LeverageRatios
from fundamental.ratios.efficiency import EfficiencyRatios


class HistoricalAnalyzer:
    """
    Calculates financial ratios for any mapped financial statement.
    Used for historical comparisons such as Piotroski F-Score.
    """

    def __init__(self):
        self.profitability = ProfitabilityRatios()
        self.liquidity = LiquidityRatios()
        self.leverage = LeverageRatios()
        self.efficiency = EfficiencyRatios()

    def analyze(self, mapped):

        revenue = mapped.get("revenue")
        gross_profit = mapped.get("gross_profit")
        operating_income = mapped.get("operating_income")
        net_income = mapped.get("net_income")
        ebit = mapped.get("ebit")

        total_assets = mapped.get("total_assets")
        shareholder_equity = mapped.get("shareholder_equity")

        current_assets = mapped.get("current_assets")
        current_liabilities = mapped.get("current_liabilities")

        inventory = mapped.get("inventory")
        cash = mapped.get("cash")
        total_debt = mapped.get("total_debt")

        operating_cash_flow = mapped.get("operating_cash_flow")

        accounts_receivable = mapped.get("accounts_receivable")

        profitability = {

            "gross_margin": self.profitability.gross_margin(
                gross_profit,
                revenue,
            ),

            "operating_margin": self.profitability.operating_margin(
                operating_income,
                revenue,
            ),

            "net_margin": self.profitability.net_margin(
                net_income,
                revenue,
            ),

            "roe": self.profitability.return_on_equity(
                net_income,
                shareholder_equity,
            ),

            "roa": self.profitability.return_on_assets(
                net_income,
                total_assets,
            ),

            "roce": self.profitability.return_on_capital_employed(
                ebit,
                total_assets,
                current_liabilities,
            ),
        }

        liquidity = {

            "current_ratio": self.liquidity.current_ratio(
                current_assets,
                current_liabilities,
            ),

            "quick_ratio": self.liquidity.quick_ratio(
                current_assets,
                inventory,
                current_liabilities,
            ),

            "cash_ratio": self.liquidity.cash_ratio(
                cash,
                current_liabilities,
            ),
        }

        leverage = {

            "debt_to_equity": self.leverage.debt_to_equity(
                total_debt,
                shareholder_equity,
            ),

            "debt_to_assets": self.leverage.debt_to_assets(
                total_debt,
                total_assets,
            ),

            "equity_ratio": self.leverage.equity_ratio(
                shareholder_equity,
                total_assets,
            ),
        }

        efficiency = {

            "asset_turnover": self.efficiency.asset_turnover(
                revenue,
                total_assets,
            ),

            "inventory_turnover": self.efficiency.inventory_turnover(
                revenue,
                inventory,
            ),

            "receivables_turnover": self.efficiency.receivables_turnover(
                revenue,
                accounts_receivable,
            ),

            "working_capital_turnover": self.efficiency.working_capital_turnover(
                revenue,
                current_assets,
                current_liabilities,
            ),
        }

        return {

            "profitability": profitability,
            "liquidity": liquidity,
            "leverage": leverage,
            "efficiency": efficiency,

            # Raw values
            "net_income": net_income,
            "operating_cash_flow": operating_cash_flow,
            "total_debt": total_debt,
            "shares_outstanding": mapped.get("shares_outstanding"),

            # Keep complete mapped values
            "mapped": mapped,
        }