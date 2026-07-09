from fundamental.ratios.valuation import ValuationRatios


class ValuationAnalyzer:
    """
    Performs valuation analysis.
    """

    def __init__(self):
        self.ratios = ValuationRatios()

    def analyze(
        self,
        company,
        mapped,
        growth,
    ):

        market_cap = company.get("market_cap")
        price = company.get("current_price")
        eps = company.get("eps")
        shares_outstanding = company.get("shares_outstanding")

        total_debt = mapped.get("total_debt")
        cash = mapped.get("cash")

        revenue = mapped.get("revenue")
        ebitda = mapped.get("ebitda")

        shareholder_equity = mapped.get("shareholder_equity")

        # Book Value Per Share
        if (
            shareholder_equity is not None
            and shares_outstanding not in (None, 0)
        ):
            book_value_per_share = (
                shareholder_equity / shares_outstanding
            )
        else:
            book_value_per_share = None

        # Valuation Ratios
        pe = self.ratios.pe_ratio(
            price,
            eps,
        )

        pb = self.ratios.pb_ratio(
            price,
            book_value_per_share,
        )

        ps = self.ratios.ps_ratio(
            market_cap,
            revenue,
        )

        peg = self.ratios.peg_ratio(
            pe,
            growth.get("eps_growth"),
        )

        ev = self.ratios.enterprise_value(
            market_cap,
            total_debt,
            cash,
        )

        ev_ebitda = self.ratios.ev_to_ebitda(
            ev,
            ebitda,
        )

        return {
            "pe_ratio": pe,
            "pb_ratio": pb,
            "ps_ratio": ps,
            "peg_ratio": peg,
            "enterprise_value": ev,
            "ev_to_ebitda": ev_ebitda,
        }