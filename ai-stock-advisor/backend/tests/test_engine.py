import pytest
from conftest import client

# Companies to validate
TICKERS = [
    "MSFT",
    "AAPL",
    "NVDA",
    "TSLA",
    "JPM",
    "GOOGL",
    "META",
    "AMZN",
    "KO",
    "PEP",
]

EXPECTED_ANALYZERS = [
    "profitability",
    "growth",
    "liquidity",
    "leverage",
    "valuation",
    "cashflow",
    "financial_health",
    "efficiency",
    "piotroski",
    "altman",
    "beneish",
    "dupont",
    "dcf",
    "peter_lynch",
    "owner_earnings",
    "graham",
    "ev_multiple",
    "buffett",
    "magic_formula",
    "economic_moat",
    "dividend_quality",
    "shareholder_yield",
    "earnings_quality",
    "roic",
    "share_dilution",
    "capital_allocation",
    "reinvestment_rate",
    "capex_efficiency",
    "cash_conversion_cycle",
    "revenue_stability",
    "earnings_stability",
    "eps_consistency",
    "margin_stability",
    "debt_maturity",
    "debt_service_coverage",
    "interest_rate_risk",
    "working_capital_quality",
    "insider_ownership",
    "institutional_ownership",
    "insider_trading",
    "management_quality",
    "pricing_power",
    "market_leadership",
    "brand_strength",
    "rd_efficiency",
    "residual_income",
    "eva",
    "fcf_yield",
    "croic",
]

@pytest.mark.parametrize("ticker", TICKERS)
def test_company_analysis(ticker):

    response = client.get(f"/company/{ticker}")

    assert response.status_code == 200

    data = response.json()

    assert "analysis" in data

    analysis = data["analysis"]

    for analyzer in EXPECTED_ANALYZERS:
        assert analyzer in analysis, f"{ticker}: Missing analyzer '{analyzer}'"

        result = analysis[analyzer]

        assert isinstance(result, dict), (
            f"{ticker}: {analyzer} should return a dictionary"
        )

        assert "score" in result, (
            f"{ticker}: {analyzer} missing score"
        )

        assert "max_score" in result, (
            f"{ticker}: {analyzer} missing max_score"
        )

        score = result["score"]

        assert isinstance(score, (int, float)), (
            f"{ticker}: {analyzer} score is not numeric"
        )

        assert 0 <= score <= result["max_score"], (
            f"{ticker}: {analyzer} invalid score"
        )