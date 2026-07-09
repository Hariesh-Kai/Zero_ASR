from typing import List, Dict
import yfinance as yf


class CompanySearchService:
    """
    Searches companies using Yahoo Finance.
    """

    def search(self, query: str) -> List[Dict]:

        try:
            results = yf.Search(query).quotes

            companies = []

            for item in results:

                companies.append({
                    "symbol": item.get("symbol"),
                    "name": item.get("shortname"),
                    "exchange": item.get("exchange"),
                    "type": item.get("quoteType"),
                })

            return companies

        except Exception:
            return []