from services.company_service import CompanyService

from data.financial_data import FinancialData

from financials.income import IncomeStatement
from financials.balance import BalanceSheet
from financials.cashflow import CashFlow
from financials.report import FinancialReport


class FinancialEngine:

    def __init__(self):

        self.company = CompanyService()

        self.financial_data = FinancialData()

    def analyze(
        self,
        ticker: str,
    ):

        company = self.company.get_company(
            ticker
        )

        financials = self.financial_data.load(
            ticker
        )

        income = IncomeStatement.parse(
            financials["income_statement"]
        )

        balance = BalanceSheet.parse(
            financials["balance_sheet"]
        )

        cashflow = CashFlow.parse(
            financials["cash_flow"]
        )

        return FinancialReport.build(

            company,

            income,

            balance,

            cashflow,

        )