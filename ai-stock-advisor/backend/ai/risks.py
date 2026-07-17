class RiskAnalyzer:
    """
    Identifies the company's biggest risks
    using analysis scores.
    """

    def generate(
        self,
        analysis,
        scores,
    ):

        risks = []

        # ------------------------------------
        # Valuation
        # ------------------------------------

        if scores.get("valuation", 100) <= 40:
            risks.append(
                "The stock appears expensive based on valuation metrics."
            )

        # ------------------------------------
        # DCF
        # ------------------------------------

        if scores.get("dcf", 100) <= 40:
            risks.append(
                "Current market price is above estimated intrinsic value."
            )

        # ------------------------------------
        # Free Cash Flow Yield
        # ------------------------------------

        if scores.get("fcf_yield", 100) <= 40:
            risks.append(
                "Free cash flow yield is relatively low."
            )

        # ------------------------------------
        # Share Dilution
        # ------------------------------------

        if scores.get("share_dilution", 100) <= 40:
            risks.append(
                "Existing shareholders may face dilution."
            )

        # ------------------------------------
        # Shareholder Yield
        # ------------------------------------

        if scores.get("shareholder_yield", 100) <= 40:
            risks.append(
                "Shareholder returns through dividends and buybacks are limited."
            )

        # ------------------------------------
        # Insider Ownership
        # ------------------------------------

        if scores.get("insider_ownership", 100) <= 40:
            risks.append(
                "Low insider ownership may reduce management alignment with shareholders."
            )

        # ------------------------------------
        # Insider Trading
        # ------------------------------------

        if scores.get("insider_trading", 100) <= 40:
            risks.append(
                "Recent insider trading activity may warrant further review."
            )

        # ------------------------------------
        # Working Capital
        # ------------------------------------

        if scores.get("working_capital_quality", 100) <= 40:
            risks.append(
                "Working capital quality is weaker than desired."
            )

        # ------------------------------------
        # Financial Health
        # ------------------------------------

        if scores.get("financial_health", 100) <= 40:
            risks.append(
                "Financial health indicators suggest elevated risk."
            )

        # ------------------------------------
        # No significant risks
        # ------------------------------------

        if not risks:
            risks.append(
                "No major financial risks were identified based on the current analysis."
            )

        return risks