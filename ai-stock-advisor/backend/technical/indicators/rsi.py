import pandas as pd

from technical.indicators.base_indicator import BaseIndicator


class RSIIndicator(BaseIndicator):
    """
    Relative Strength Index (RSI)
    """

    def calculate(
        self,
        df: pd.DataFrame,
        period: int = 14,
    ):

        self.validate(df)

        result = self.copy(df)

        delta = result["close"].diff()

        gain = delta.clip(lower=0)

        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(period).mean()

        avg_loss = loss.rolling(period).mean()

        rs = avg_gain / avg_loss

        result["rsi"] = 100 - (
            100 / (1 + rs)
        )

        return result

    def latest_value(
        self,
        df: pd.DataFrame,
        period: int = 14,
    ):

        result = self.calculate(df, period)

        value = super().latest(
            result["rsi"]
        )

        signal = "Neutral"

        if value is not None:

            if value >= 70:
                signal = "Overbought"

            elif value <= 30:
                signal = "Oversold"

        return {

            "indicator": "RSI",

            "period": period,

            "value": value,

            "signal": signal,
        }