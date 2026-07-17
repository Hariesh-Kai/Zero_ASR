import yfinance as yf


class CompanyService:
    """
    Provides company profile information.

    Used by:
    - Fundamental Engine
    - Financial Engine
    - Advisor Engine
    - Valuation Engine
    """

    def get_company(
        self,
        ticker: str,
    ):

        stock = yf.Ticker(ticker)

        info = stock.info

        dividend_yield = info.get("dividendYield")

        return {

            # -----------------------------------
            # Basic Company Information
            # -----------------------------------

            "ticker": ticker.upper(),

            "company": info.get("longName"),

            "sector": info.get("sector"),

            "industry": info.get("industry"),

            "country": info.get("country"),

            "currency": info.get("currency"),

            "website": info.get("website"),

            # -----------------------------------
            # Market Data
            # -----------------------------------

            "current_price": info.get("currentPrice"),

            "market_cap": info.get("marketCap"),

            "enterprise_value": info.get("enterpriseValue"),

            "shares_outstanding": info.get("sharesOutstanding"),

            "beta": info.get("beta"),

            # -----------------------------------
            # Financial Position
            # -----------------------------------

            "total_cash": info.get("totalCash"),

            "total_debt": info.get("totalDebt"),

            "free_cash_flow": info.get("freeCashflow"),

            "operating_cash_flow": info.get("operatingCashflow"),

            # -----------------------------------
            # Valuation
            # -----------------------------------

            "eps": info.get("trailingEps"),

            "forward_eps": info.get("forwardEps"),

            "pe_ratio": info.get("trailingPE"),

            "forward_pe": info.get("forwardPE"),

            "peg_ratio": info.get("pegRatio"),

            "earnings_growth": info.get("earningsGrowth"),

            "price_to_book": info.get("priceToBook"),

            "book_value": info.get("bookValue"),

            "return_on_equity": info.get("returnOnEquity"),

            "enterprise_to_ebitda": info.get("enterpriseToEbitda"),

            "ebitda": info.get("ebitda"),

            # -----------------------------------
            # Dividend
            # -----------------------------------

            "dividend_yield": dividend_yield,

            "payout_ratio": info.get("payoutRatio"),

            # -----------------------------------
            # Trading
            # -----------------------------------

            "previous_close": info.get("previousClose"),

            "open": info.get("open"),

            "day_high": info.get("dayHigh"),

            "day_low": info.get("dayLow"),

            "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),

            "fifty_two_week_low": info.get("fiftyTwoWeekLow"),

            "volume": info.get("volume"),

            "average_volume": info.get("averageVolume"),

        }