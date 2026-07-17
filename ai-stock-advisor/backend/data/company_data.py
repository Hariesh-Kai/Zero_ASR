from data.cache import CompanyCache
from data_providers.yahoo_finance import YahooFinanceProvider


class CompanyData:
    """
    Centralized company data loader.

    Downloads company data once,
    caches it,
    and returns it to every engine.
    """

    def __init__(self):

        self.provider = YahooFinanceProvider()

    def load(
        self,
        ticker: str,
    ):

        ticker = ticker.upper()

        # -----------------------------
        # Cache
        # -----------------------------

        if CompanyCache.has(ticker):

            return CompanyCache.get(
                ticker
            )

        # -----------------------------
        # Download
        # -----------------------------

        data = self.provider.get_complete_company(
            ticker
        )

        # -----------------------------
        # Save
        # -----------------------------

        CompanyCache.set(
            ticker,
            data,
        )

        return data

    def refresh(
        self,
        ticker: str,
    ):

        ticker = ticker.upper()

        data = self.provider.get_complete_company(
            ticker
        )

        CompanyCache.set(
            ticker,
            data,
        )

        return data

    def clear(self):

        CompanyCache.clear()