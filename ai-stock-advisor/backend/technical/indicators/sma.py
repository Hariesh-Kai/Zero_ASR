import pandas as pd

from technical.indicators.base_indicator import BaseIndicator


class SMAIndicator(BaseIndicator):
    """
    Simple Moving Average (SMA)
    """

    def calculate(
        self,
        df: pd.DataFrame,
        period: int = 20,
    ):

        self.validate(df)

        result = self.copy(df)

        column = f"sma_{period}"

        result[column] = (
            result["close"]
            .rolling(window=period)
            .mean()
        )

        return result

    def latest_value(
        self,
        df: pd.DataFrame,
        period: int = 20,
    ):

        result = self.calculate(df, period)

        return {
            "period": period,
            "value": super().latest(result[f"sma_{period}"]),
        }