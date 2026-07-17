import pandas as pd

from technical.indicators.base_indicator import BaseIndicator


class EMAIndicator(BaseIndicator):
    """
    Exponential Moving Average (EMA)
    """

    def calculate(
        self,
        df: pd.DataFrame,
        period: int = 20,
    ):

        self.validate(df)

        result = self.copy(df)

        column = f"ema_{period}"

        result[column] = (
            result["close"]
            .ewm(
                span=period,
                adjust=False,
            )
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
            "indicator": "EMA",
            "period": period,
            "value": super().latest(
                result[f"ema_{period}"]
            ),
        }