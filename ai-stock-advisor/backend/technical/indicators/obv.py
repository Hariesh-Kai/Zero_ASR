import pandas as pd

from technical.indicators.base_indicator import BaseIndicator


class OBVIndicator(BaseIndicator):
    """
    On Balance Volume (OBV)
    """

    def calculate(
        self,
        df: pd.DataFrame,
    ):

        self.validate(df)

        result = self.copy(df)

        obv = [0]

        for i in range(1, len(result)):

            if result["close"].iloc[i] > result["close"].iloc[i - 1]:
                obv.append(
                    obv[-1] + result["volume"].iloc[i]
                )

            elif result["close"].iloc[i] < result["close"].iloc[i - 1]:
                obv.append(
                    obv[-1] - result["volume"].iloc[i]
                )

            else:
                obv.append(obv[-1])

        result["obv"] = obv

        return result

    def latest_value(
        self,
        df: pd.DataFrame,
    ):

        result = self.calculate(df)

        value = super().latest(
            result["obv"]
        )

        return {

            "indicator": "OBV",

            "value": value,
        }