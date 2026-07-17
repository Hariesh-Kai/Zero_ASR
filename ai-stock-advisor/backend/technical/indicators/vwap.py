import pandas as pd

from technical.indicators.base_indicator import BaseIndicator


class VWAPIndicator(BaseIndicator):
    """
    Volume Weighted Average Price (VWAP)
    """

    def calculate(
        self,
        df: pd.DataFrame,
    ):

        self.validate(df)

        result = self.copy(df)

        typical_price = (
            result["high"]
            + result["low"]
            + result["close"]
        ) / 3

        cumulative_tp_volume = (
            typical_price * result["volume"]
        ).cumsum()

        cumulative_volume = (
            result["volume"]
        ).cumsum()

        result["vwap"] = (
            cumulative_tp_volume
            / cumulative_volume
        )

        return result

    def latest_value(
        self,
        df: pd.DataFrame,
    ):

        result = self.calculate(df)

        close = super().latest(result["close"])

        vwap = super().latest(result["vwap"])

        if close > vwap:
            signal = "Bullish"

        elif close < vwap:
            signal = "Bearish"

        else:
            signal = "Neutral"

        return {

            "indicator": "VWAP",

            "value": vwap,

            "close": close,

            "signal": signal,
        }