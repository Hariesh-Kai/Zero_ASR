from typing import Any, Dict

import yfinance as yf


class YahooFinanceProvider:

    def __init__(self):

        self._stocks = {}

    def _get_stock(
        self,
        ticker: str,
    ):

        ticker = ticker.upper()

        if ticker not in self._stocks:

            self._stocks[ticker] = yf.Ticker(
                ticker
            )

        return self._stocks[ticker]


    def get_income_statement(self, ticker: str) -> Dict[str, Any]:
        """
        Returns the annual income statement.
        """
        stock = self._get_stock(ticker)

        try:
            return stock.financials.fillna("")
        except Exception:
            return {}

    def get_balance_sheet(self, ticker: str) -> Dict[str, Any]:
        """
        Returns the annual balance sheet.
        """
        stock = self._get_stock(ticker)

        try:
            return stock.balance_sheet.fillna("")
        except Exception:
            return {}

    def get_cash_flow(self, ticker: str) -> Dict[str, Any]:
        """
        Returns the annual cash flow statement.
        """
        stock = self._get_stock(ticker)

        try:
            return stock.cashflow.fillna("")
        except Exception:
            return {}

    def get_quarterly_income_statement(self, ticker: str) -> Dict[str, Any]:
        """
        Returns the quarterly income statement.
        """
        stock = self._get_stock(ticker)

        try:
            return stock.quarterly_financials.fillna("")
        except Exception:
            return {}

    def get_quarterly_balance_sheet(self, ticker: str) -> Dict[str, Any]:
        """
        Returns the quarterly balance sheet.
        """
        stock = self._get_stock(ticker)

        try:
            return stock.quarterly_balance_sheet.fillna("")
        except Exception:
            return {}

    def get_quarterly_cash_flow(self, ticker: str) -> Dict[str, Any]:
        """
        Returns the quarterly cash flow statement.
        """
        stock = self._get_stock(ticker)

        try:
            return stock.quarterly_cashflow.fillna("")
        except Exception:
            return {}

    def get_company(self, ticker: str) -> Dict[str, Any]:
        """
        Returns company profile information.
        """
        stock = self._get_stock(ticker)
        info = stock.info

        return {
            "ticker": ticker.upper(),
            "company": info.get("longName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "country": info.get("country"),
            "currency": info.get("currency"),
            "exchange": info.get("exchange"),

            # Company Information
            "market_cap": info.get("marketCap"),
            "employees": info.get("fullTimeEmployees"),
            "website": info.get("website"),
            "summary": info.get("longBusinessSummary"),

            # Market Data
            "current_price": info.get("currentPrice"),
            "previous_close": info.get("previousClose"),
            "open": info.get("open"),
            "day_high": info.get("dayHigh"),
            "day_low": info.get("dayLow"),
            "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
            "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
            "volume": info.get("volume"),
            "average_volume": info.get("averageVolume"),

            # Valuation Metrics
            "eps": info.get("trailingEps"),
            "forward_eps": info.get("forwardEps"),
            "pe_ratio": info.get("trailingPE"),
            "forward_pe": info.get("forwardPE"),
            "peg_ratio": info.get("pegRatio"),
            "price_to_book": info.get("priceToBook"),
            "enterprise_value": info.get("enterpriseValue"),
            "enterprise_to_ebitda": info.get("enterpriseToEbitda"),

            # Dividend
            "dividend_yield": info.get("dividendYield"),
            "payout_ratio": info.get("payoutRatio"),

            # Shares
            "shares_outstanding": info.get("sharesOutstanding"),
            "float_shares": info.get("floatShares"),
        }
    
    def get_complete_company(self, ticker: str) -> Dict[str, Any]:
        """
        Returns everything required for fundamental analysis.
        """

        return {
            "profile": self.get_company(ticker),

            "financial_statements": {
                "income_statement": self.get_income_statement(ticker),
                "balance_sheet": self.get_balance_sheet(ticker),
                "cash_flow": self.get_cash_flow(ticker),
            },

            "quarterly_financials": {
                "income_statement": self.get_quarterly_income_statement(ticker),
                "balance_sheet": self.get_quarterly_balance_sheet(ticker),
                "cash_flow": self.get_quarterly_cash_flow(ticker),
            },
        }
    
    def get_history(
        self,
        ticker: str,
        period: str = "2y",
        interval: str = "1d",
    ):

        stock = self._get_stock(
            ticker
        )

        history = stock.history(
            period=period,
            interval=interval,
            auto_adjust=True,
        )

        if not history.empty:

            history.reset_index(
                inplace=True
            )

        return history
        