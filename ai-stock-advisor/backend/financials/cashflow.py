from typing import Dict, Any
import pandas as pd


class CashFlow:
    """
    Parses Yahoo Finance cash flow statement.
    """

    @staticmethod
    def parse(cashflow: pd.DataFrame) -> Dict[str, Any]:

        if cashflow.empty:
            return {}

        latest = cashflow.iloc[:, 0]

        def convert(value):
            if value is None:
                return None

            try:
                return float(value)
            except Exception:
                return value

        operating_cf = convert(
            latest.get("Operating Cash Flow")
        )

        investing_cf = convert(
            latest.get("Investing Cash Flow")
        )

        financing_cf = convert(
            latest.get("Financing Cash Flow")
        )

        capex = convert(
            latest.get("Capital Expenditure")
        )

        free_cash_flow = None

        if operating_cf is not None and capex is not None:
            free_cash_flow = operating_cf + capex

        return {

            "operating_cash_flow": operating_cf,

            "investing_cash_flow": investing_cf,

            "financing_cash_flow": financing_cf,

            "capital_expenditure": capex,

            "free_cash_flow": free_cash_flow,

        }