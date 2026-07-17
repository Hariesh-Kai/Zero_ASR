from financials.engine import FinancialEngine


class ValuationCollector:

    def __init__(self):

        self.financials = FinancialEngine()

    def collect(
        self,
        ticker: str,
    ):

        return self.financials.analyze(
            ticker
        )