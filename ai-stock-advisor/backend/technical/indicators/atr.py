import pandas as pd

from technical.indicators.base_indicator import BaseIndicator


class ATRIndicator(BaseIndicator):
    """
    Average True Range (ATR)
    """

    def calculate(
        self,
        df: pd.DataFrame,
        period: int = 14,
    ):

        self.validate(df)

        result = self.copy(df)

        high_low = result["high"] - result["low"]

        high_close = (
            result["high"]
            - result["close"].shift()
        ).abs()

        low_close = (
            result["low"]
            - result["close"].shift()
        ).abs()

        true_range = pd.concat(
            [
                high_low,
                high_close,
                low_close,
            ],
            axis=1,
        ).max(axis=1)

        result["atr"] = (
            true_range
            .rolling(period)
            .mean()
        )

        return result

    def latest_value(
        self,
        df: pd.DataFrame,
        period: int = 14,
    ):

        result = self.calculate(df, period)

        value = super().latest(
            result["atr"]
        )

        return {

            "indicator": "ATR",

            "period": period,

            "value": value,
        }