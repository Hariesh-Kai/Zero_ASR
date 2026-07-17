import pandas as pd


class TechnicalMapper:
    """
    Converts raw Yahoo Finance data
    into a standardized format.
    """

    def map(self, df: pd.DataFrame):

        mapped = pd.DataFrame()

        mapped["date"] = pd.to_datetime(df["Date"])

        mapped["open"] = df["Open"].astype(float)

        mapped["high"] = df["High"].astype(float)

        mapped["low"] = df["Low"].astype(float)

        mapped["close"] = df["Close"].astype(float)

        mapped["volume"] = df["Volume"].astype(float)

        mapped["dividend"] = df["Dividends"].astype(float)

        mapped["split"] = df["Stock Splits"].astype(float)

        return mapped