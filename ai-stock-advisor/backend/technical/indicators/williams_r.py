import pandas as pd

from technical.indicators.base_indicator import BaseIndicator


class WilliamsRIndicator(BaseIndicator):
    """
    Williams %R Indicator
    """

    def calculate(
        self,
        df: pd.DataFrame,
        period: int = 14,
    ):

        self.validate(df)

        result = self.copy(df)

        highest_high = (
            result["high"]
            .rolling(period)
            .max()
        )

        lowest_low = (
            result["low"]
            .rolling(period)
            .min()
        )

        result["williams_r"] = (
            (
                highest_high
                - result["close"]
            )
            /
            (
                highest_high
                - lowest_low
            )
        ) * -100

        return result

    def latest_value(
        self,
        df: pd.DataFrame,
        period: int = 14,
    ):

        result = self.calculate(df, period)

        value = super().latest(
            result["williams_r"]
        )

        if value is None:
            signal = "Unknown"

        elif value >= -20:
            signal = "Overbought"

        elif value <= -80:
            signal = "Oversold"

        else:
            signal = "Neutral"

        return {

            "indicator": "Williams %R",

            "period": period,

            "value": value,

            "signal": signal,
        }