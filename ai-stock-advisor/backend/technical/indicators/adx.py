import pandas as pd
import numpy as np

from technical.indicators.base_indicator import BaseIndicator


class ADXIndicator(BaseIndicator):
    """
    Average Directional Index (ADX)
    """

    def calculate(
        self,
        df: pd.DataFrame,
        period: int = 14,
    ):

        self.validate(df)

        result = self.copy(df)

        high = result["high"]
        low = result["low"]
        close = result["close"]

        plus_dm = high.diff()

        minus_dm = -low.diff()

        plus_dm = np.where(
            (plus_dm > minus_dm) & (plus_dm > 0),
            plus_dm,
            0,
        )

        minus_dm = np.where(
            (minus_dm > plus_dm) & (minus_dm > 0),
            minus_dm,
            0,
        )

        tr = pd.concat(
            [
                high - low,
                (high - close.shift()).abs(),
                (low - close.shift()).abs(),
            ],
            axis=1,
        ).max(axis=1)

        atr = tr.rolling(period).mean()

        plus_di = (
            100
            * pd.Series(plus_dm).rolling(period).mean()
            / atr
        )

        minus_di = (
            100
            * pd.Series(minus_dm).rolling(period).mean()
            / atr
        )

        dx = (
            (plus_di - minus_di).abs()
            / (plus_di + minus_di)
        ) * 100

        result["adx"] = dx.rolling(period).mean()

        return result

    def latest_value(
        self,
        df: pd.DataFrame,
        period: int = 14,
    ):

        result = self.calculate(df, period)

        value = super().latest(result["adx"])

        if value is None:
            strength = "Unknown"

        elif value < 20:
            strength = "Weak"

        elif value < 25:
            strength = "Developing"

        elif value < 50:
            strength = "Strong"

        elif value < 75:
            strength = "Very Strong"

        else:
            strength = "Extremely Strong"

        return {
            "indicator": "ADX",
            "period": period,
            "value": value,
            "strength": strength,
        }