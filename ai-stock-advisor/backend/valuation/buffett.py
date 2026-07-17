class BuffettModel:
    """
    Warren Buffett Quality Analysis.
    """

    def analyze(
        self,
        data,
    ):

        company = data["company"]

        score = 0

        reasons = []

        # --------------------------
        # ROE
        # --------------------------

        roe = company.get(
            "return_on_equity"
        )

        if roe and roe >= 0.15:

            score += 20

            reasons.append(
                "High Return on Equity"
            )

        # --------------------------
        # Debt
        # --------------------------

        debt = company.get(
            "total_debt"
        ) or 0

        cash = company.get(
            "total_cash"
        ) or 0

        if cash >= debt:

            score += 20

            reasons.append(
                "Strong Balance Sheet"
            )

        # --------------------------
        # Positive Cash Flow
        # --------------------------

        operating_cf = company.get(
            "operating_cash_flow"
        )

        if operating_cf and operating_cf > 0:

            score += 20

            reasons.append(
                "Positive Operating Cash Flow"
            )

        # --------------------------
        # Profitability
        # --------------------------

        if company.get("eps"):

            score += 20

            reasons.append(
                "Profitable Business"
            )

        # --------------------------
        # Dividend
        # --------------------------

        dividend = company.get(
            "dividend_yield"
        )

        if dividend and dividend > 0:

            score += 20

            reasons.append(
                "Returns Cash to Shareholders"
            )

        # --------------------------

        if score >= 80:

            rating = "Excellent"

        elif score >= 60:

            rating = "Good"

        elif score >= 40:

            rating = "Average"

        else:

            rating = "Poor"

        return {

            "model": "Buffett",

            "score": score,

            "rating": rating,

            "reasons": reasons,

        }