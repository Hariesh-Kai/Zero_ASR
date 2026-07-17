import pandas as pd

from technical.indicators.base_indicator import BaseIndicator


class MACDIndicator(BaseIndicator):
    """
    Moving Average Convergence Divergence (MACD)
    """

    def calculate(
        self,
        df: pd.DataFrame,
        fast_period: int = 12,
        slow_period: int = 26,
        signal_period: int = 9,
    ):

        self.validate(df)

        result = self.copy(df)

        ema_fast = (
            result["close"]
            .ewm(span=fast_period, adjust=False)
            .mean()
        )

        ema_slow = (
            result["close"]
            .ewm(span=slow_period, adjust=False)
            .mean()
        )

        result["macd"] = ema_fast - ema_slow

        result["signal"] = (
            result["macd"]
            .ewm(span=signal_period, adjust=False)
            .mean()
        )

        result["histogram"] = (
            result["macd"] - result["signal"]
        )

        return result

    def latest_value(
        self,
        df: pd.DataFrame,
    ):

        result = self.calculate(df)

        macd = super().latest(result["macd"])
        signal = super().latest(result["signal"])
        histogram = super().latest(result["histogram"])

        if macd is None or signal is None:
            status = "Unknown"

        elif macd > signal:
            status = "Bullish"

        elif macd < signal:
            status = "Bearish"

        else:
            status = "Neutral"

        return {

            "indicator": "MACD",

            "macd": macd,

            "signal_line": signal,

            "histogram": histogram,

            "signal": status,
        }