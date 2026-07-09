class ValuationRatios:
    """
    Valuation ratio calculations.
    """

    @staticmethod
    def pe_ratio(price, eps):
        if eps is None or eps <= 0:
            return None
        return price / eps

    @staticmethod
    def pb_ratio(price, book_value_per_share):
        if book_value_per_share is None or book_value_per_share <= 0:
            return None
        return price / book_value_per_share

    @staticmethod
    def ps_ratio(market_cap, revenue):
        if revenue is None or revenue <= 0:
            return None
        return market_cap / revenue

    @staticmethod
    def peg_ratio(pe_ratio, earnings_growth):
        if earnings_growth is None or earnings_growth <= 0:
            return None
        return pe_ratio / earnings_growth

    @staticmethod
    def enterprise_value(
        market_cap,
        total_debt,
        cash,
    ):
        market_cap = market_cap or 0
        total_debt = total_debt or 0
        cash = cash or 0

        return market_cap + total_debt - cash

    @staticmethod
    def ev_to_ebitda(ev, ebitda):
        if ebitda is None or ebitda <= 0:
            return None
        return ev / ebitda