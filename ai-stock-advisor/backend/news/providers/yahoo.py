import yfinance as yf


class YahooNewsProvider:
    """
    Collects company news from Yahoo Finance.
    """

    def fetch(self, ticker: str):

        stock = yf.Ticker(ticker)

        news = stock.news

        return news