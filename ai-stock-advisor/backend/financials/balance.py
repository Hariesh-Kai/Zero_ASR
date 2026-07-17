from typing import Dict, Any
import pandas as pd


class BalanceSheet:
    """
    Parses Yahoo Finance balance sheet.
    """

    @staticmethod
    def parse(balance: pd.DataFrame) -> Dict[str, Any]:

        if balance.empty:
            return {}

        latest = balance.iloc[:, 0]

        def convert(value):
            if value is None:
                return None

            try:
                return float(value)
            except Exception:
                return value

        return {

            "cash": convert(
                latest.get("Cash And Cash Equivalents")
            ),

            "short_term_investments": convert(
                latest.get("Other Short Term Investments")
            ),

            "current_assets": convert(
                latest.get("Current Assets")
            ),

            "total_assets": convert(
                latest.get("Total Assets")
            ),

            "current_liabilities": convert(
                latest.get("Current Liabilities")
            ),

            "total_liabilities": convert(
                latest.get("Total Liabilities Net Minority Interest")
            ),

            "long_term_debt": convert(
                latest.get("Long Term Debt")
            ),

            "stockholders_equity": convert(
                latest.get("Stockholders Equity")
            ),

            "inventory": convert(
                latest.get("Inventory")
            ),

            "goodwill": convert(
                latest.get("Goodwill")
            ),

        }