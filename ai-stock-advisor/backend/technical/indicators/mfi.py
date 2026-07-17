import pandas as pd

from technical.indicators.base_indicator import BaseIndicator


class MFIIndicator(BaseIndicator):
    """
    Money Flow Index (MFI)
    """

    def calculate(
        self,
        df: pd.DataFrame,
        period: int = 14,
    ):

        self.validate(df)

        result = self.copy(df)

        typical_price = (
            result["high"]
            + result["low"]
            + result["close"]
        ) / 3

        money_flow = (
            typical_price
            * result["volume"]
        )

        positive_flow = [0]
        negative_flow = [0]

        for i in range(1, len(result)):

            if typical_price.iloc[i] > typical_price.iloc[i - 1]:

                positive_flow.append(
                    money_flow.iloc[i]
                )

                negative_flow.append(0)

            else:

                positive_flow.append(0)

                negative_flow.append(
                    money_flow.iloc[i]
                )

        positive_mf = (
            pd.Series(positive_flow)
            .rolling(period)
            .sum()
        )

        negative_mf = (
            pd.Series(negative_flow)
            .rolling(period)
            .sum()
        )

        money_ratio = (
            positive_mf
            / negative_mf
        )

        result["mfi"] = (
            100
            - (
                100
                / (1 + money_ratio)
            )
        )

        return result

    def latest_value(
        self,
        df: pd.DataFrame,
        period: int = 14,
    ):

        result = self.calculate(df, period)

        value = super().latest(
            result["mfi"]
        )

        if value is None:
            signal = "Unknown"

        elif value >= 80:
            signal = "Overbought"

        elif value <= 20:
            signal = "Oversold"

        else:
            signal = "Neutral"

        return {

            "indicator": "MFI",

            "period": period,

            "value": value,

            "signal": signal,
        }