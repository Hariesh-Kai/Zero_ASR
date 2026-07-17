from typing import Dict, Any
import pandas as pd


class IncomeStatement:
    """
    Parses Yahoo Finance income statement data.
    """

    @staticmethod
    def parse(income: pd.DataFrame) -> Dict[str, Any]:

        if income.empty:
            return {}

        latest = income.iloc[:, 0]

        def convert(value):
            if value is None:
                return None

            try:
                return float(value)
            except Exception:
                return value

        return {

            "revenue": convert(
                latest.get("Total Revenue")
            ),

            "cost_of_revenue": convert(
                latest.get("Cost Of Revenue")
            ),

            "gross_profit": convert(
                latest.get("Gross Profit")
            ),

            "operating_expense": convert(
                latest.get("Operating Expense")
            ),

            "operating_income": convert(
                latest.get("Operating Income")
            ),

            "pretax_income": convert(
                latest.get("Pretax Income")
            ),

            "net_income": convert(
                latest.get("Net Income")
            ),

            "eps": convert(
                latest.get("Diluted EPS")
            ),

            "ebit": convert(
                latest.get("EBIT")
            ),

            "ebitda": convert(
                latest.get("EBITDA")
            ),

        }