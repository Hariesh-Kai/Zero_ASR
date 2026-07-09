from conftest import client


def test_jpm_all_analyzers():

    response = client.get(
        "/company/JPM"
    )

    assert response.status_code == 200

    data = response.json()

    analysis = data["analysis"]

    expected = [

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

    for analyzer in expected:
        assert analyzer in analysis