import pandas as pd

from technical.indicators.base_indicator import BaseIndicator


class BollingerBandsIndicator(BaseIndicator):
    """
    Bollinger Bands
    """

    def calculate(
        self,
        df: pd.DataFrame,
        period: int = 20,
        std_dev: int = 2,
    ):

        self.validate(df)

        result = self.copy(df)

        sma = (
            result["close"]
            .rolling(period)
            .mean()
        )

        std = (
            result["close"]
            .rolling(period)
            .std()
        )

        result["middle_band"] = sma

        result["upper_band"] = sma + (
            std * std_dev
        )

        result["lower_band"] = sma - (
            std * std_dev
        )

        return result

    def latest_value(
        self,
        df: pd.DataFrame,
        period: int = 20,
    ):

        result = self.calculate(df, period)

        close = super().latest(result["close"])

        upper = super().latest(result["upper_band"])

        middle = super().latest(result["middle_band"])

        lower = super().latest(result["lower_band"])

        if close >= upper:
            signal = "Overbought"

        elif close <= lower:
            signal = "Oversold"

        else:
            signal = "Neutral"

        return {

            "indicator": "Bollinger Bands",

            "period": period,

            "upper_band": upper,

            "middle_band": middle,

            "lower_band": lower,

            "close": close,

            "signal": signal,
        }