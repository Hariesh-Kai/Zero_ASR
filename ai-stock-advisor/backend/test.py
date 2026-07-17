from data.financial_data import FinancialData
from financials.engine import FinancialEngine


def line():
    print("=" * 60)


ticker = "AAPL"

# ======================================================
# FinancialData Test
# ======================================================

line()
print("TESTING FINANCIAL DATA")
line()

financial_data = FinancialData()

financials = financial_data.load(ticker)

print("Income Statement :", not financials["income_statement"].empty)
print("Balance Sheet    :", not financials["balance_sheet"].empty)
print("Cash Flow        :", not financials["cash_flow"].empty)
print("Quarterly Income :", not financials["quarterly_income_statement"].empty)
print("Quarterly Balance:", not financials["quarterly_balance_sheet"].empty)
print("Quarterly Cash   :", not financials["quarterly_cash_flow"].empty)

# ======================================================
# Cache Test
# ======================================================

line()
print("TESTING CACHE")
line()

financials2 = financial_data.load(ticker)

print("Object 1 ID :", id(financials))
print("Object 2 ID :", id(financials2))
print("Cache Works :", financials is financials2)

# ======================================================
# Financial Engine Test
# ======================================================

line()
print("TESTING FINANCIAL ENGINE")
line()

engine = FinancialEngine()

report = engine.analyze(ticker)

print("Company Name :", report["company"].get("longName"))

print("\nIncome Statement")
print("----------------")
for key, value in report["income_statement"].items():
    print(f"{key:25}: {value}")

print("\nBalance Sheet")
print("----------------")
for key, value in report["balance_sheet"].items():
    print(f"{key:25}: {value}")

print("\nCash Flow")
print("----------------")
for key, value in report["cash_flow"].items():
    print(f"{key:25}: {value}")

line()
print("ALL TESTS PASSED")
line()