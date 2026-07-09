from fundamental.ratios.altman import AltmanRatios


class AltmanAnalyzer:
    """
    Calculates the Altman Z-Score and bankruptcy risk.
    """

    def __init__(self):
        self.ratios = AltmanRatios()

    def analyze(
        self,
        mapped,
    ):

        # Financial data
        current_assets = mapped.get("current_assets")
        current_liabilities = mapped.get("current_liabilities")
        total_assets = mapped.get("total_assets")

        retained_earnings = mapped.get("retained_earnings")
        ebit = mapped.get("ebit")

        market_cap = mapped.get("market_cap")
        total_liabilities = mapped.get("total_liabilities")

        revenue = mapped.get("revenue")

        # ---------------------------------------
        # Altman Components
        # ---------------------------------------

        a = self.ratios.working_capital_to_assets(
            current_assets,
            current_liabilities,
            total_assets,
        )

        b = self.ratios.retained_earnings_to_assets(
            retained_earnings,
            total_assets,
        )

        c = self.ratios.ebit_to_assets(
            ebit,
            total_assets,
        )

        d = self.ratios.market_value_equity_to_liabilities(
            market_cap,
            total_liabilities,
        )

        e = self.ratios.sales_to_assets(
            revenue,
            total_assets,
        )

        # ---------------------------------------
        # Final Z-Score
        # ---------------------------------------

        z_score = self.ratios.z_score(
            a,
            b,
            c,
            d,
            e,
        )

        # ---------------------------------------
        # Risk Classification
        # ---------------------------------------

        if z_score is None:
            risk = "Unknown"

        elif z_score > 2.99:
            risk = "Safe"

        elif z_score >= 1.81:
            risk = "Grey Zone"

        else:
            risk = "Distress"

        return {

            "working_capital_to_assets": a,
            "retained_earnings_to_assets": b,
            "ebit_to_assets": c,
            "market_value_equity_to_liabilities": d,
            "sales_to_assets": e,

            "z_score": z_score,
            "risk": risk,
        }