from data.cache import CompanyCache
from data_providers.yahoo_finance import YahooFinanceProvider

class MarketData:
    """
    Provides historical market data for a company.

    Uses CompanyCache so historical prices
    are downloaded only once.
    """

    def __init__(self):

        self.provider = YahooFinanceProvider()

    def load(
        self,
        ticker: str,
        period: str = "2y",
        interval: str = "1d",
    ):

        cache_key = (
            f"{ticker.upper()}_history_{period}_{interval}"
        )

        if CompanyCache.has(cache_key):

            return CompanyCache.get(cache_key)

        history = self.provider.get_history(
            ticker=ticker,
            period=period,
            interval=interval,
        )

        CompanyCache.set(
            cache_key,
            history,
        )

        return history

    def refresh(
        self,
        ticker: str,
        period: str = "2y",
        interval: str = "1d",
    ):

        cache_key = (
            f"{ticker.upper()}_history_{period}_{interval}"
        )

        history = self.provider.get_history(
            ticker=ticker,
            period=period,
            interval=interval,
        )

        CompanyCache.set(
            cache_key,
            history,
        )

        return history