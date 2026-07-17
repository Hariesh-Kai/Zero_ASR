import yfinance as yf


class ChartService:
    """
    Provides historical stock price data for charts.
    """

    def get_chart(
        self,
        ticker: str,
        period: str = "6mo",
    ):

        stock = yf.Ticker(ticker)

        history = stock.history(period=period)

        data = []

        for date, row in history.iterrows():

            data.append({

                "date": date.strftime("%Y-%m-%d"),

                "open": round(float(row["Open"]), 2),

                "high": round(float(row["High"]), 2),

                "low": round(float(row["Low"]), 2),

                "close": round(float(row["Close"]), 2),

                "volume": int(row["Volume"]),

            })

        return data