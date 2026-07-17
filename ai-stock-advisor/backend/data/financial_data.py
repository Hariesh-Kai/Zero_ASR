from data.cache import CompanyCache
from data_providers.yahoo_finance import YahooFinanceProvider


class FinancialData:
    """
    Loads financial statements from Yahoo Finance.

    Uses CompanyCache to avoid repeated downloads.
    """

    def __init__(self):

        self.provider = YahooFinanceProvider()

    def load(
        self,
        ticker: str,
    ):

        cache_key = (
            f"{ticker.upper()}_financials"
        )

        if CompanyCache.has(cache_key):

            return CompanyCache.get(
                cache_key
            )

        financials = self.load_uncached(
            ticker
        )

        CompanyCache.set(
            cache_key,
            financials,
        )

        return financials

    def refresh(
        self,
        ticker: str,
    ):

        cache_key = (
            f"{ticker.upper()}_financials"
        )

        financials = self.load_uncached(
            ticker
        )

        CompanyCache.set(
            cache_key,
            financials,
        )

        return financials

    def load_uncached(
        self,
        ticker: str,
    ):

        return {

            "income_statement":
                self.provider.get_income_statement(
                    ticker
                ),

            "balance_sheet":
                self.provider.get_balance_sheet(
                    ticker
                ),

            "cash_flow":
                self.provider.get_cash_flow(
                    ticker
                ),

            "quarterly_income_statement":
                self.provider.get_quarterly_income_statement(
                    ticker
                ),

            "quarterly_balance_sheet":
                self.provider.get_quarterly_balance_sheet(
                    ticker
                ),

            "quarterly_cash_flow":
                self.provider.get_quarterly_cash_flow(
                    ticker
                ),
        }