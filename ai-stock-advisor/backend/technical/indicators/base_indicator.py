from abc import ABC
import pandas as pd


class BaseIndicator(ABC):
    """
    Base class for all technical indicators.
    """

    REQUIRED_COLUMNS = [
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]

    @staticmethod
    def validate(df: pd.DataFrame):

        missing = [
            col
            for col in BaseIndicator.REQUIRED_COLUMNS
            if col not in df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing columns: {missing}"
            )

    @staticmethod
    def copy(df: pd.DataFrame):

        return df.copy()

    @staticmethod
    def latest(series: pd.Series):

        if series.empty:
            return None

        return float(series.iloc[-1])

    @staticmethod
    def latest_n(series: pd.Series, n: int):

        if len(series) < n:
            return series

        return series.tail(n)