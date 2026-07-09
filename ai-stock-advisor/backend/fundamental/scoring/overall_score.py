class OverallScore:
    """
    Calculates the overall fundamental score.
    Only considers scores that have actually been calculated.
    """

    @staticmethod
    def calculate(
        profitability,
        growth,
        liquidity,
        leverage,
        valuation,
        cashflow,
        efficiency,
        financial_health,
        piotroski,
        altman,
        beneish,
        dupont,
        dcf,
        peter_lynch,
        owner_earnings,
        graham,
        ev_multiple,
        buffett,
        magic_formula,
        economic_moat,
        dividend_quality,
        shareholder_yield,
        earnings_quality,
        roic,
        share_dilution,
        capital_allocation,
        reinvestment_rate,
        capex_efficiency,
        cash_conversion_cycle,
        revenue_stability,
        earnings_stability,
        eps_consistency,
        margin_stability,
        debt_maturity,
        debt_service_coverage,
        interest_rate_risk,
        working_capital_quality,
        insider_ownership,
        institutional_ownership,
        insider_trading,
        management_quality,
        pricing_power,
        market_leadership,
        brand_strength,
        rd_efficiency,
        residual_income,
        eva,
        fcf_yield,
        croic,
    ):
        scores = []

        if profitability is not None:
            scores.append(profitability)

        if growth is not None:
            scores.append(growth)

        if liquidity is not None:
            scores.append(liquidity)

        if leverage is not None:
            scores.append(leverage)

        if valuation is not None:
            scores.append(valuation)

        if cashflow is not None:
            scores.append(cashflow)

        if efficiency is not None:
            scores.append(efficiency)

        if financial_health is not None:
            scores.append(financial_health)

        if piotroski is not None:
            scores.append(piotroski)

        if altman is not None:
            scores.append(altman)

        if beneish is not None:
            scores.append(beneish)
        
        if dupont is not None:
             scores.append(dupont)

        if dcf is not None:
            scores.append(dcf)

        if peter_lynch is not None:
            scores.append(peter_lynch)
        
        if owner_earnings is not None:
            scores.append(owner_earnings)
        
        if graham is not None:
            scores.append(graham)
        
        if ev_multiple is not None:
            scores.append(ev_multiple)
        
        if buffett is not None:
            scores.append(buffett)

        if magic_formula is not None:
            scores.append(magic_formula)
        
        if economic_moat is not None:
            scores.append(economic_moat)
        
        if dividend_quality is not None:
            scores.append(dividend_quality)
        
        if shareholder_yield is not None:
            scores.append(shareholder_yield)
        
        if earnings_quality is not None:
            scores.append(earnings_quality)

        if roic is not None:
            scores.append(roic)

        if share_dilution is not None:
            scores.append(share_dilution)

        if capital_allocation is not None:
            scores.append(capital_allocation)

        if reinvestment_rate is not None:
            scores.append(reinvestment_rate)

        if capex_efficiency is not None:
            scores.append(capex_efficiency)
        
        if cash_conversion_cycle is not None:
            scores.append(cash_conversion_cycle)
        
        if revenue_stability is not None:
            scores.append(revenue_stability)
        
        if earnings_stability is not None:
            scores.append(earnings_stability)
        
        if eps_consistency is not None:
            scores.append(eps_consistency)

        if margin_stability is not None:
            scores.append(margin_stability)

        if debt_maturity is not None:
            scores.append(debt_maturity)

        if debt_service_coverage is not None:
            scores.append(debt_service_coverage)
        
        if interest_rate_risk is not None:
            scores.append(interest_rate_risk)

        if working_capital_quality is not None:
            scores.append(working_capital_quality)   
        
        if insider_ownership is not None:
            scores.append(insider_ownership)

        if institutional_ownership is not None:
            scores.append(institutional_ownership)
        
        if insider_trading is not None:
            scores.append(insider_trading)

        if management_quality is not None:
            scores.append(management_quality)

        if pricing_power is not None:
            scores.append(pricing_power)
        
        if market_leadership is not None:
            scores.append(market_leadership)
        
        if brand_strength is not None:
            scores.append(brand_strength)
        
        if rd_efficiency is not None:
            scores.append(rd_efficiency)
        
        if residual_income is not None:
            scores.append(residual_income)

        if eva is not None:
            scores.append(eva)
        
        if fcf_yield is not None:
            scores.append(fcf_yield)

        if croic is not None:
            scores.append(croic)
        
        if len(scores) == 0:
            overall = 0
        else:
            overall = sum(scores) / len(scores)
        

        # -----------------------------
        # Recommendation
        # -----------------------------

        if overall >= 90:
            recommendation = "Strong Buy"

        elif overall >= 80:
            recommendation = "Buy"

        elif overall >= 65:
            recommendation = "Hold"

        elif overall >= 50:
            recommendation = "Sell"

        else:
            recommendation = "Strong Sell"

        return {
            "overall_score": round(overall, 2),
            "recommendation": recommendation,
        }