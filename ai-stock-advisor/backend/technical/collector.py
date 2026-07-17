from data.market_data import MarketData


class TechnicalCollector:
    """
    Downloads historical OHLCV market data.
    """

    def __init__(self):

        self.market = MarketData()

    def collect(
        self,
        ticker: str,
        period: str = "2y",
        interval: str = "1d",
    ):

        return self.market.load(
            ticker=ticker,
            period=period,
            interval=interval,
        )