from typing import Dict, Any


class FinancialReport:
    """
    Builds the final financial report.
    """

    @staticmethod
    def build(

        company: Dict[str, Any],

        income: Dict[str, Any],

        balance: Dict[str, Any],

        cashflow: Dict[str, Any],

    ):

        return {

            "company": company,

            "income_statement": income,

            "balance_sheet": balance,

            "cash_flow": cashflow,

        }