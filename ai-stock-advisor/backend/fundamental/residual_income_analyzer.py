class ResidualIncomeAnalyzer:
    """
    Estimates intrinsic value using
    the Residual Income model.
    """

    @staticmethod
    def _safe(value):
        return 0 if value is None else value

    def analyze(
        self,
        mapped,
    ):

        net_income = self._safe(
            mapped.get("net_income")
        )

        equity = self._safe(
            mapped.get("shareholder_equity")
        )

        market_cap = self._safe(
            mapped.get("market_cap")
        )

        cost_of_equity = 0.10

        equity_charge = (
            equity * cost_of_equity
        )

        residual_income = (
            net_income - equity_charge
        )

        intrinsic_value = (
            equity + residual_income
        )

        valuation = "Fair"

        if intrinsic_value > market_cap:
            valuation = "Undervalued"

        elif intrinsic_value < market_cap:
            valuation = "Overvalued"

        return {
            "intrinsic_value": intrinsic_value,
            "market_cap": market_cap,
            "residual_income": residual_income,
            "cost_of_equity": cost_of_equity,
            "valuation": valuation,
        }