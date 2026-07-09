class DividendQualityAnalyzer:
    """
    Evaluates the quality and sustainability
    of a company's dividend.
    """

    @staticmethod
    def _safe(value):
        return 0 if value is None else value

    def analyze(
        self,
        profile,
        mapped,
    ):

        dividend_yield = self._safe(
            profile.get("dividend_yield")
        )

        payout_ratio = self._safe(
            profile.get("payout_ratio")
        )

        # Yahoo Finance sometimes returns payout ratio
        # as a decimal (0.207 = 20.7%)
        if (
            payout_ratio is not None
            and payout_ratio <= 1
        ):
            payout_ratio *= 100

        free_cash_flow = self._safe(
            mapped.get("free_cash_flow")
        )

        net_income = self._safe(
            mapped.get("net_income")
        )

        dividend_coverage = None

        if payout_ratio > 0:

            dividend_coverage = (
                100 / payout_ratio
            )

        score = 0

        # Healthy Yield
        if 1 <= dividend_yield <= 5:
            score += 1

        # Healthy Payout
        if 20 <= payout_ratio <= 60:
            score += 1

        # Positive Free Cash Flow
        if free_cash_flow > 0:
            score += 1

        # Positive Earnings
        if net_income > 0:
            score += 1

        # Coverage
        if (
            dividend_coverage is not None
            and dividend_coverage >= 2
        ):
            score += 1

        if score == 5:
            quality = "Excellent"

        elif score == 4:
            quality = "Good"

        elif score == 3:
            quality = "Average"

        elif score == 2:
            quality = "Weak"

        else:
            quality = "Poor"

        return {
            "score": score,
            "max_score": 5,
            "dividend_yield": dividend_yield,
            "payout_ratio": payout_ratio,
            "dividend_coverage": dividend_coverage,
            "quality": quality,
        }