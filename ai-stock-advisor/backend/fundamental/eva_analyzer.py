class EVAAnalyzer:
    """
    Calculates Economic Value Added (EVA).
    """

    @staticmethod
    def _safe(value):
        return 0 if value is None else value

    def analyze(
        self,
        mapped,
    ):

        ebit = self._safe(
            mapped.get("ebit")
        )

        total_debt = self._safe(
            mapped.get("total_debt")
        )

        shareholder_equity = self._safe(
            mapped.get("shareholder_equity")
        )

        tax_rate = 0.21
        wacc = 0.10

        nopat = ebit * (1 - tax_rate)

        invested_capital = (
            total_debt +
            shareholder_equity
        )

        capital_charge = (
            invested_capital * wacc
        )

        eva = (
            nopat - capital_charge
        )

        if eva > 0:
            quality = "Value Creator"
        else:
            quality = "Value Destroyer"

        return {
            "eva": eva,
            "nopat": nopat,
            "invested_capital": invested_capital,
            "capital_charge": capital_charge,
            "quality": quality,
        }