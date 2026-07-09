class CashConversionCycleAnalyzer:
    """
    Measures how quickly a company converts
    inventory and receivables into cash.
    """

    @staticmethod
    def _safe(value):
        return 0 if value is None else value

    def analyze(self, mapped):

        inventory = self._safe(
            mapped.get("inventory")
        )

        accounts_receivable = self._safe(
            mapped.get("accounts_receivable")
        )

        current_liabilities = self._safe(
            mapped.get("current_liabilities")
        )

        revenue = self._safe(
            mapped.get("revenue")
        )

        cost_of_revenue = revenue - self._safe(
            mapped.get("gross_profit")
        )

        dsi = 0
        dso = 0
        dpo = 0

        if cost_of_revenue > 0:
            dsi = (
                inventory
                / cost_of_revenue
            ) * 365

        if revenue > 0:
            dso = (
                accounts_receivable
                / revenue
            ) * 365

        if cost_of_revenue > 0:
            dpo = (
                current_liabilities
                / cost_of_revenue
            ) * 365

        ccc = dsi + dso - dpo

        score = 1

        if ccc <= 20:
            score = 5

        elif ccc <= 40:
            score = 4

        elif ccc <= 60:
            score = 3

        elif ccc <= 90:
            score = 2

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
            "days_inventory": dsi,
            "days_sales_outstanding": dso,
            "days_payables": dpo,
            "cash_conversion_cycle": ccc,
            "quality": quality,
        }