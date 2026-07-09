class EVMultipleAnalyzer:
    """
    Enterprise Value Multiple Analysis.

    Compares EV/EBITDA with standard valuation ranges.
    """

    @staticmethod
    def analyze(mapped):

        enterprise_value = mapped.get("market_cap")

        total_debt = mapped.get("total_debt") or 0
        cash = mapped.get("cash") or 0

        if enterprise_value:
            enterprise_value = enterprise_value + total_debt - cash

        ebitda = mapped.get("ebitda")

        if (
            enterprise_value is None
            or ebitda is None
            or ebitda <= 0
        ):
            return {
                "enterprise_value": enterprise_value,
                "ev_to_ebitda": None,
                "valuation": "Unknown",
            }

        multiple = enterprise_value / ebitda

        if multiple < 8:
            valuation = "Undervalued"

        elif multiple < 12:
            valuation = "Fairly Valued"

        else:
            valuation = "Overvalued"

        return {
            "enterprise_value": enterprise_value,
            "ev_to_ebitda": multiple,
            "valuation": valuation,
        }