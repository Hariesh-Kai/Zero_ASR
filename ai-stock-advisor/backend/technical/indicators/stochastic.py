import pandas as pd

from technical.indicators.base_indicator import BaseIndicator


class StochasticIndicator(BaseIndicator):
    """
    Stochastic Oscillator
    """

    def calculate(
        self,
        df: pd.DataFrame,
        period: int = 14,
        smooth: int = 3,
    ):

        self.validate(df)

        result = self.copy(df)

        lowest_low = (
            result["low"]
            .rolling(period)
            .min()
        )

        highest_high = (
            result["high"]
            .rolling(period)
            .max()
        )

        result["percent_k"] = (
            (
                result["close"] - lowest_low
            )
            /
            (
                highest_high - lowest_low
            )
        ) * 100

        result["percent_d"] = (
            result["percent_k"]
            .rolling(smooth)
            .mean()
        )

        return result

    def latest_value(
        self,
        df: pd.DataFrame,
        period: int = 14,
    ):

        result = self.calculate(df, period)

        k = super().latest(result["percent_k"])
        d = super().latest(result["percent_d"])

        if k is None:
            signal = "Unknown"

        elif k >= 80:
            signal = "Overbought"

        elif k <= 20:
            signal = "Oversold"

        else:
            signal = "Neutral"

        return {

            "indicator": "Stochastic",

            "period": period,

            "%K": k,

            "%D": d,

            "signal": signal,
        }