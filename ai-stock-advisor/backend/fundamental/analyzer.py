from fundamental.ratios.profitability import ProfitabilityRatios
from fundamental.ratios.liquidity import LiquidityRatios
from fundamental.ratios.leverage import LeverageRatios


class FundamentalAnalyzer:

    def __init__(self):
        self.profitability = ProfitabilityRatios()
        self.liquidity = LiquidityRatios()
        self.leverage = LeverageRatios()

    def analyze(self, data):

        income = data.get("latest_income", {})
        balance = data.get("latest_balance", {})
        cashflow = data.get("latest_cash_flow", {})

        revenue = income.get("Total Revenue", 0)
        gross_profit = income.get("Gross Profit", 0)
        operating_income = income.get("Operating Income", 0)
        net_income = income.get("Net Income", 0)
        ebit = income.get("EBIT", 0)

        total_assets = balance.get("Total Assets", 0)
        shareholder_equity = balance.get("Stockholders Equity", 0)

        current_assets = balance.get("Current Assets", 0)
        current_liabilities = balance.get("Current Liabilities", 0)

        inventory = balance.get("Inventory", 0)

        cash = balance.get(
            "Cash And Cash Equivalents",
            0,
        )

        total_debt = balance.get("Total Debt", 0)

        return {

            "profitability": {

                "gross_margin":
                    self.profitability.gross_margin(
                        gross_profit,
                        revenue,
                    ),

                "operating_margin":
                    self.profitability.operating_margin(
                        operating_income,
                        revenue,
                    ),

                "net_margin":
                    self.profitability.net_margin(
                        net_income,
                        revenue,
                    ),

                "roe":
                    self.profitability.return_on_equity(
                        net_income,
                        shareholder_equity,
                    ),

                "roa":
                    self.profitability.return_on_assets(
                        net_income,
                        total_assets,
                    ),

                "roce":
                    self.profitability.return_on_capital_employed(
                        ebit,
                        total_assets,
                        current_liabilities,
                    ),
            },

            "liquidity": {

                "current_ratio":
                    self.liquidity.current_ratio(
                        current_assets,
                        current_liabilities,
                    ),

                "quick_ratio":
                    self.liquidity.quick_ratio(
                        current_assets,
                        inventory,
                        current_liabilities,
                    ),

                "cash_ratio":
                    self.liquidity.cash_ratio(
                        cash,
                        current_liabilities,
                    ),
            },

            "leverage": {

                "debt_to_equity":
                    self.leverage.debt_to_equity(
                        total_debt,
                        shareholder_equity,
                    ),

                "debt_to_assets":
                    self.leverage.debt_to_assets(
                        total_debt,
                        total_assets,
                    ),

                "equity_ratio":
                    self.leverage.equity_ratio(
                        shareholder_equity,
                        total_assets,
                    ),
            }
        }