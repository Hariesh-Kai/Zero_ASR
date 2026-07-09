import yfinance as yf

stock = yf.Ticker("MSFT")

print("\n========== INCOME ==========\n")
print(stock.financials.index.tolist())

print("\n========== BALANCE ==========\n")
print(stock.balance_sheet.index.tolist())

print("\n========== CASH FLOW ==========\n")
print(stock.cashflow.index.tolist())