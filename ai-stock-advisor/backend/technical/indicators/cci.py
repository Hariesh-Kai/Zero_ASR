import pandas as pd

from technical.indicators.base_indicator import BaseIndicator


class CCIIndicator(BaseIndicator):
    """
    Commodity Channel Index (CCI)
    """

    def calculate(
        self,
        df: pd.DataFrame,
        period: int = 20,
    ):

        self.validate(df)

        result = self.copy(df)

        typical_price = (
            result["high"]
            + result["low"]
            + result["close"]
        ) / 3

        sma = (
            typical_price
            .rolling(period)
            .mean()
        )

        mean_deviation = (
            typical_price
            .rolling(period)
            .apply(
                lambda x: (x - x.mean()).abs().mean(),
                raw=False,
            )
        )

        result["cci"] = (
            typical_price - sma
        ) / (
            0.015 * mean_deviation
        )

        return result

    def latest_value(
        self,
        df: pd.DataFrame,
        period: int = 20,
    ):

        result = self.calculate(df, period)

        value = super().latest(
            result["cci"]
        )

        if value is None:
            signal = "Unknown"

        elif value >= 100:
            signal = "Bullish"

        elif value <= -100:
            signal = "Bearish"

        else:
            signal = "Neutral"

        return {
            "indicator": "CCI",
            "period": period,
            "value": value,
            "signal": signal,
        }