class DupontAnalyzer:
    """
    Performs DuPont Analysis.

    ROE = Net Profit Margin × Asset Turnover × Equity Multiplier
    """

    @staticmethod
    def _safe_divide(a, b):
        if a is None or b in (None, 0):
            return None
        return a / b

    def analyze(self, mapped):

        revenue = mapped.get("revenue")
        net_income = mapped.get("net_income")
        total_assets = mapped.get("total_assets")
        shareholder_equity = mapped.get("shareholder_equity")

        # ----------------------------------
        # DuPont Components
        # ----------------------------------

        net_profit_margin = self._safe_divide(
            net_income,
            revenue,
        )

        asset_turnover = self._safe_divide(
            revenue,
            total_assets,
        )

        equity_multiplier = self._safe_divide(
            total_assets,
            shareholder_equity,
        )

        # ----------------------------------
        # ROE
        # ----------------------------------

        roe = None

        if (
            net_profit_margin is not None
            and asset_turnover is not None
            and equity_multiplier is not None
        ):
            roe = (
                net_profit_margin
                * asset_turnover
                * equity_multiplier
                * 100
            )

        # ----------------------------------
        # Quality
        # ----------------------------------

        if roe is None:
            quality = "Unknown"

        elif roe >= 25:
            quality = "Excellent"

        elif roe >= 18:
            quality = "Strong"

        elif roe >= 12:
            quality = "Average"

        else:
            quality = "Weak"

        return {

            "net_profit_margin": (
                net_profit_margin * 100
                if net_profit_margin is not None
                else None
            ),

            "asset_turnover": asset_turnover,

            "equity_multiplier": equity_multiplier,

            "roe": roe,

            "quality": quality,
        }