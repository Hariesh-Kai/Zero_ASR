from fundamental.ratios.beneish import BeneishRatios


class BeneishAnalyzer:
    """
    Calculates the Beneish M-Score.

    Lower than -2.22  -> Unlikely Manipulator
    Higher than -2.22 -> Possible Manipulator
    """

    def __init__(self):
        self.ratios = BeneishRatios()

    def analyze(
        self,
        current,
        previous,
    ):

        # -----------------------------
        # Current Financials
        # -----------------------------

        revenue = current.get("revenue")
        receivables = current.get("accounts_receivable")
        gross_profit = current.get("gross_profit")

        total_assets = current.get("total_assets")
        current_assets = current.get("current_assets")
        ppe = current.get("property_plant_equipment")

        # -----------------------------
        # Previous Financials
        # -----------------------------

        previous_revenue = previous.get("revenue")
        previous_receivables = previous.get("accounts_receivable")
        previous_gross_profit = previous.get("gross_profit")

        previous_assets = previous.get("total_assets")
        previous_current_assets = previous.get("current_assets")
        previous_ppe = previous.get("property_plant_equipment")

        # -----------------------------
        # Ratios
        # -----------------------------

        dsri = self.ratios.dsri(
            receivables,
            previous_receivables,
            revenue,
            previous_revenue,
        )

        gmi = self.ratios.gmi(
            revenue,
            gross_profit,
            previous_revenue,
            previous_gross_profit,
        )

        aqi = self.ratios.aqi(
            total_assets,
            current_assets,
            ppe,
            previous_assets,
            previous_current_assets,
            previous_ppe,
        )

        sgi = self.ratios.sgi(
            revenue,
            previous_revenue,
        )

        m_score = self.ratios.m_score(
            dsri,
            gmi,
            aqi,
            sgi,
        )

        # -----------------------------
        # Interpretation
        # -----------------------------

        if m_score is None:
            risk = "Unknown"

        elif m_score < -2.22:
            risk = "Unlikely Manipulator"

        else:
            risk = "Possible Manipulator"

        return {

            "dsri": dsri,
            "gmi": gmi,
            "aqi": aqi,
            "sgi": sgi,

            "m_score": m_score,
            "risk": risk,
        }