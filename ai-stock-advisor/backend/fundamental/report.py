from typing import Dict, Any


class FundamentalReport:
    """
    Builds the final response returned to the frontend.
    """

    @staticmethod
    def build(
        company: Dict[str, Any],
        analysis: Dict[str, Any],
        scores: Dict[str, Any],
        recommendation: Dict[str, Any],
    ) -> Dict[str, Any]:

        return {

            "company": {
                "ticker": company.get("ticker"),
                "name": company.get("name") or company.get("company"),
                "sector": company.get("sector"),
                "industry": company.get("industry"),
                "country": company.get("country"),
                "currency": company.get("currency"),
                "market_cap": company.get("market_cap"),
                "website": company.get("website"),
            },

            "analysis": analysis,

            "scores": {
                "profitability": scores.get("profitability"),
                "growth": scores.get("growth"),
                "liquidity": scores.get("liquidity"),
                "leverage": scores.get("leverage"),
                "valuation": scores.get("valuation"),
                "cashflow": scores.get("cashflow"),
                "efficiency": scores.get("efficiency"),
                "financial_health": scores.get("financial_health"),
                "piotroski": scores.get("piotroski"),
                "altman": scores.get("altman"),
                "beneish": scores.get("beneish"),
                "dupont": scores.get("dupont"),
                "dcf": scores.get("dcf"),
                "peter_lynch": scores.get("peter_lynch"),
                "owner_earnings": scores.get("owner_earnings"),
                "graham": scores.get("graham"),
                "ev_multiple": scores.get("ev_multiple"),
                "buffett": scores.get("buffett"),
                "magic_formula": scores.get("magic_formula"),
                "economic_moat": scores.get("economic_moat"),
                "dividend_quality": scores.get("dividend_quality"),
                "shareholder_yield": scores.get("shareholder_yield"),
                "earnings_quality": scores.get("earnings_quality"),
                "roic": scores.get("roic"),
                "share_dilution": scores.get("share_dilution"),
                "capital_allocation": scores.get("capital_allocation"),
                "reinvestment_rate": scores.get("reinvestment_rate"),
                "capex_efficiency": scores.get("capex_efficiency"),
                "cash_conversion_cycle": scores.get("cash_conversion_cycle"),
                "revenue_stability": scores.get("revenue_stability"),
                "earnings_stability": scores.get("earnings_stability"),
                "eps_consistency": scores.get("eps_consistency"),
                "margin_stability": scores.get("margin_stability"),
                "debt_maturity": scores.get("debt_maturity"),
                "debt_service_coverage": scores.get("debt_service_coverage"),
                "interest_rate_risk": scores.get("interest_rate_risk"),
                "working_capital_quality": scores.get("working_capital_quality"),
                "insider_ownership": scores.get("insider_ownership"),
                "institutional_ownership": scores.get("institutional_ownership"),
                "insider_trading": scores.get("insider_trading"),
                "management_quality": scores.get("management_quality"),
                "pricing_power": scores.get("pricing_power"),
                "market_leadership": scores.get("market_leadership"),
                "brand_strength": scores.get("brand_strength"),
                "rd_efficiency": scores.get("rd_efficiency"),
                "residual_income": scores.get("residual_income"),
                "eva": scores.get("eva"),
                "fcf_yield": scores.get("fcf_yield"),
                "croic": scores.get("croic"),
                "overall": scores.get("overall"),
            },
                        
            "recommendation": recommendation,
        }