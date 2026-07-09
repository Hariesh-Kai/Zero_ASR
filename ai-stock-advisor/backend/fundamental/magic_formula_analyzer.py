class MagicFormulaAnalyzer:
    """
    Joel Greenblatt Magic Formula.

    Combines:
    1. Earnings Yield
    2. Return on Capital
    """

    @staticmethod
    def _safe(value):
        return 0 if value is None else value

    def analyze(self, mapped):

        ebit = self._safe(mapped.get("ebit"))
        enterprise_value = self._safe(mapped.get("market_cap"))

        total_debt = self._safe(mapped.get("total_debt"))
        cash = self._safe(mapped.get("cash"))

        enterprise_value = enterprise_value + total_debt - cash

        net_working_capital = (
            self._safe(mapped.get("current_assets"))
            - self._safe(mapped.get("current_liabilities"))
        )

        fixed_assets = self._safe(
            mapped.get("property_plant_equipment")
        )

        invested_capital = (
            net_working_capital
            + fixed_assets
        )

        earnings_yield = None
        roc = None

        if enterprise_value > 0:
            earnings_yield = (
                ebit / enterprise_value
            ) * 100

        if invested_capital > 0:
            roc = (
                ebit / invested_capital
            ) * 100

        if (
            earnings_yield is not None
            and roc is not None
        ):

            if earnings_yield >= 8 and roc >= 20:
                quality = "Excellent"

            elif earnings_yield >= 6 and roc >= 15:
                quality = "Very Good"

            elif earnings_yield >= 4 and roc >= 10:
                quality = "Good"

            else:
                quality = "Poor"

        else:

            quality = "Unknown"

        return {
            "earnings_yield": earnings_yield,
            "return_on_capital": roc,
            "quality": quality,
        }