from typing import Any, Dict
import math


class FinancialMapper:
    """
    Maps Yahoo Finance financial statements into
    standardized values used by the analysis engine.
    """
    
    @staticmethod
    def _first(data: Dict[str, Any], *keys):
        """
        Returns the first matching key found.
        Converts missing values to None.
        """

        for key in keys:

            if key not in data:
                continue

            value = data[key]

            if value is None:
                return None

            if isinstance(value, str):

                value = value.strip()

                if value == "":
                    return None

                if value.upper() == "N/A":
                    return None

            if isinstance(value, float):

                if math.isnan(value):
                    return None

            return value

        return None

    @staticmethod
    def map(financials: Dict[str, Any]) -> Dict[str, Any]:

        income = financials.get("income_statement", {})
        balance = financials.get("balance_sheet", {})
        cashflow = financials.get("cash_flow", {})

        return {

            # =====================================================
            # Income Statement
            # =====================================================

            "revenue": FinancialMapper._first(
                income,
                "Total Revenue",
                "Revenue",
            ),

            "gross_profit": FinancialMapper._first(
                income,
                "Gross Profit",
            ),

            "operating_income": FinancialMapper._first(
                income,
                "Operating Income",
            ),

            "net_income": FinancialMapper._first(
                income,
                "Net Income",
                "Net Income Common Stockholders",
            ),

            "eps": FinancialMapper._first(
                income,
                "Diluted EPS",
                "Basic EPS",
            ),

            "ebit": FinancialMapper._first(
                income,
                "EBIT",
            ),

            "ebitda": FinancialMapper._first(
                income,
                "EBITDA",
                "Normalized EBITDA",
            ),

            "interest_expense": FinancialMapper._first(
                income,
                "Interest Expense",
                "Interest Expense Non Operating",
            ),

            "selling_general_admin": FinancialMapper._first(
                income,
                "Selling General And Administration",
                "Selling And Marketing Expense",
                "Selling General Administrative",
            ),

            "research_and_development": FinancialMapper._first(
                income,
                "Research And Development",
                "Research Development",
            ),

            "depreciation": FinancialMapper._first(
                income,
                "Reconciled Depreciation",
                "Depreciation",
                "Depreciation Amortization Depletion",
            ),

            "income_from_operations": FinancialMapper._first(
                income,
                "Operating Income",
            ),


            # =====================================================
            # Balance Sheet
            # =====================================================

            "total_assets": FinancialMapper._first(
                balance,
                "Total Assets",
            ),

            "current_assets": FinancialMapper._first(
                balance,
                "Current Assets",
            ),

            "current_liabilities": FinancialMapper._first(
                balance,
                "Current Liabilities",
                "Current Liabilities Net Minority Interest",
            ),

            "total_liabilities": FinancialMapper._first(
                balance,
                "Total Liabilities Net Minority Interest",
                "Total Liabilities",
            ),

            "inventory": FinancialMapper._first(
                balance,
                "Inventory",
            ),

            "cash": FinancialMapper._first(
                balance,
                "Cash And Cash Equivalents",
                "Cash Cash Equivalents And Short Term Investments",
            ),

            "total_debt": FinancialMapper._first(
                balance,
                "Total Debt",
            ),

            "shareholder_equity": FinancialMapper._first(
                balance,
                "Stockholders Equity",
                "Total Equity Gross Minority Interest",
                "Common Stock Equity",
            ),

            "retained_earnings": FinancialMapper._first(
                balance,
                "Retained Earnings",
            ),

            "accounts_receivable": FinancialMapper._first(
                balance,
                "Accounts Receivable",
                "Gross Accounts Receivable",
                "Receivables",
            ),

            "property_plant_equipment": FinancialMapper._first(
                balance,
                "Net PPE",
                "Property Plant Equipment",
                "Properties",
                "Net Property Plant Equipment",
            ),

            "current_investments": FinancialMapper._first(
                balance,
                "Other Short Term Investments",
                "Available For Sale Securities",
            ),

            "long_term_investments": FinancialMapper._first(
                balance,
                "Long Term Investments",
                "Investments And Advances",
            ),

            # NEW: Needed for Piotroski, share dilution analysis, etc.
            "shares_outstanding": FinancialMapper._first(
                balance,
                "Ordinary Shares Number",
                "Share Issued",
            ),

            # =====================================================
            # Cash Flow Statement
            # =====================================================

            "operating_cash_flow": FinancialMapper._first(
                cashflow,
                "Operating Cash Flow",
                "OperatingCashFlow",
                "Cash Flow From Continuing Operating Activities",
            ),

            "capital_expenditure": FinancialMapper._first(
                cashflow,
                "Capital Expenditure",
                "Capital Expenditure Reported",
                "Purchase Of PPE",
            ),

            "depreciation_cashflow": FinancialMapper._first(
                cashflow,
                "Depreciation And Amortization",
                "Depreciation",
            ),

            "free_cash_flow": FinancialMapper._first(
                cashflow,
                "Free Cash Flow",
            ),

            # =====================================================
            # Company Information
            # =====================================================

            "market_cap": financials.get("market_cap"),

            "current_price": financials.get("current_price"),
            
        }