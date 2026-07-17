class DCFAssumptions:
    """
    Default assumptions used by the DCF model.

    These values can later be customized
    by industry, country, or user.
    """

    def get(self):

        return {

            # Forecast Horizon

            "forecast_years": 10,

            # Revenue Growth

            "high_growth_years": 5,

            "high_growth_rate": 0.10,

            "stable_growth_rate": 0.03,

            # Operating Margin

            "target_operating_margin": 0.42,

            # Tax

            "tax_rate": 0.21,

            # Reinvestment

            "sales_to_capital": 2.5,

            # Cost of Capital

            "risk_free_rate": 0.045,

            "market_return": 0.10,

            "beta": 1.00,

            "cost_of_debt": 0.05,

            "debt_ratio": 0.15,

            "equity_ratio": 0.85,

            # Terminal

            "terminal_growth": 0.025,

        }