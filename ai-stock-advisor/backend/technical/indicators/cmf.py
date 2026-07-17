import pandas as pd

from technical.indicators.base_indicator import BaseIndicator


class CMFIndicator(BaseIndicator):
    """
    Chaikin Money Flow (CMF)
    """

    def calculate(
        self,
        df: pd.DataFrame,
        period: int = 20,
    ):

        self.validate(df)

        result = self.copy(df)

        money_flow_multiplier = (
            (
                (result["close"] - result["low"])
                -
                (result["high"] - result["close"])
            )
            /
            (
                result["high"] - result["low"]
            )
        )

        money_flow_multiplier = money_flow_multiplier.fillna(0)

        money_flow_volume = (
            money_flow_multiplier
            * result["volume"]
        )

        result["cmf"] = (
            money_flow_volume
            .rolling(period)
            .sum()
            /
            result["volume"]
            .rolling(period)
            .sum()
        )

        return result

    def latest_value(
        self,
        df: pd.DataFrame,
        period: int = 20,
    ):

        result = self.calculate(df, period)

        value = super().latest(
            result["cmf"]
        )

        if value is None:
            signal = "Unknown"

        elif value > 0:
            signal = "Bullish"

        elif value < 0:
            signal = "Bearish"

        else:
            signal = "Neutral"

        return {

            "indicator": "CMF",

            "period": period,

            "value": value,

            "signal": signal,
        }