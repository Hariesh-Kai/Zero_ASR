from typing import Any, Dict
import pandas as pd

from fundamental.financial_mapper import FinancialMapper


class FinancialExtractor:
    """
    Extracts financial statements while preserving:

    1. Complete financial history
    2. Latest financial statements
    3. Previous financial statements
    4. Standardized mapped values
    """

    @staticmethod
    def _latest(statement):

        if statement is None:
            return {}

        if isinstance(statement, pd.DataFrame):

            if statement.empty:
                return {}

            return statement.iloc[:, 0].to_dict()

        if isinstance(statement, dict):

            if len(statement) == 0:
                return {}

            latest_period = list(statement.keys())[0]

            return statement[latest_period]

        return {}

    @staticmethod
    def _previous(statement):

        if statement is None:
            return {}

        if isinstance(statement, pd.DataFrame):

            if statement.empty:
                return {}

            if statement.shape[1] < 2:
                return {}

            return statement.iloc[:, 1].to_dict()

        if isinstance(statement, dict):

            if len(statement) < 2:
                return {}

            previous_period = list(statement.keys())[1]

            return statement[previous_period]

        return {}

    @staticmethod
    def extract(
        financial_data: Dict[str, Any],
        company: Dict[str, Any],
    ) -> Dict[str, Any]:

        income = financial_data.get(
            "financial_statements",
            {}
        ).get(
            "income_statement",
            {}
        )

        balance = financial_data.get(
            "financial_statements",
            {}
        ).get(
            "balance_sheet",
            {}
        )

        cashflow = financial_data.get(
            "financial_statements",
            {}
        ).get(
            "cash_flow",
            {}
        )

        latest_income = FinancialExtractor._latest(income)
        latest_balance = FinancialExtractor._latest(balance)
        latest_cashflow = FinancialExtractor._latest(cashflow)

        previous_income = FinancialExtractor._previous(income)
        previous_balance = FinancialExtractor._previous(balance)
        previous_cashflow = FinancialExtractor._previous(cashflow)

        mapped = FinancialMapper.map(
            {
                "income_statement": latest_income,
                "balance_sheet": latest_balance,
                "cash_flow": latest_cashflow,
                "market_cap": company.get("market_cap"),
                "current_price": company.get("current_price"),
            }
        )

        previous_mapped = FinancialMapper.map(
            {
                "income_statement": previous_income,
                "balance_sheet": previous_balance,
                "cash_flow": previous_cashflow,
                "market_cap": company.get("market_cap"),
                "current_price": company.get("current_price"),
            }
        )

        return {
            "income_statement": income,
            "balance_sheet": balance,
            "cash_flow": cashflow,

            "latest_income": latest_income,
            "latest_balance": latest_balance,
            "latest_cash_flow": latest_cashflow,

            "previous_income": previous_income,
            "previous_balance": previous_balance,
            "previous_cash_flow": previous_cashflow,

            "mapped": mapped,
            "previous_mapped": previous_mapped,
        }