from data.cache import CompanyCache
from news.providers.yahoo import YahooNewsProvider


class NewsData:
    """
    Provides company news.

    Uses CompanyCache so news is downloaded
    only once during the cache lifetime.
    """

    def __init__(self):

        self.provider = YahooNewsProvider()

    def load(
        self,
        ticker: str,
    ):

        cache_key = f"{ticker.upper()}_news"

        if CompanyCache.has(cache_key):

            return CompanyCache.get(cache_key)

        news = self.provider.fetch(
            ticker
        )

        CompanyCache.set(
            cache_key,
            news,
        )

        return news

    def refresh(
        self,
        ticker: str,
    ):

        cache_key = f"{ticker.upper()}_news"

        news = self.provider.fetch(
            ticker
        )

        CompanyCache.set(
            cache_key,
            news,
        )

        return news