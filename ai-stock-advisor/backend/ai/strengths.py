class StrengthAnalyzer:
    """
    Identifies the company's biggest strengths
    using the analysis and scores.
    """

    def generate(
        self,
        analysis,
        scores,
    ):

        strengths = []

        # ------------------------------------
        # Profitability
        # ------------------------------------

        if scores.get("profitability", 0) >= 80:
            strengths.append(
                "Exceptional profitability with strong margins and returns."
            )

        # ------------------------------------
        # Growth
        # ------------------------------------

        if scores.get("growth", 0) >= 80:
            strengths.append(
                "Strong revenue and earnings growth."
            )

        # ------------------------------------
        # Financial Health
        # ------------------------------------

        if scores.get("financial_health", 0) >= 80:
            strengths.append(
                "Excellent financial health with low financial risk."
            )

        # ------------------------------------
        # Cash Flow
        # ------------------------------------

        if scores.get("cashflow", 0) >= 80:
            strengths.append(
                "Consistently strong cash flow generation."
            )

        # ------------------------------------
        # Economic Moat
        # ------------------------------------

        if scores.get("economic_moat", 0) >= 80:
            strengths.append(
                "Possesses a durable competitive advantage."
            )

        # ------------------------------------
        # ROIC
        # ------------------------------------

        if scores.get("roic", 0) >= 80:
            strengths.append(
                "Excellent capital allocation and high return on invested capital."
            )

        # ------------------------------------
        # Management
        # ------------------------------------

        if scores.get("management_quality", 0) >= 80:
            strengths.append(
                "Management demonstrates efficient capital allocation."
            )

        # ------------------------------------
        # Pricing Power
        # ------------------------------------

        if scores.get("pricing_power", 0) >= 80:
            strengths.append(
                "Strong pricing power supports healthy margins."
            )

        # ------------------------------------
        # Brand
        # ------------------------------------

        if scores.get("brand_strength", 0) >= 80:
            strengths.append(
                "Strong brand recognition provides competitive advantages."
            )

        # ------------------------------------
        # Market Leadership
        # ------------------------------------

        if scores.get("market_leadership", 0) >= 80:
            strengths.append(
                "Industry-leading market position."
            )

        return strengths