from fundamental.scoring.profitability_score import ProfitabilityScore
from fundamental.scoring.liquidity_score import LiquidityScore
from fundamental.scoring.leverage_score import LeverageScore
from fundamental.scoring.valuation_score import ValuationScore
from fundamental.scoring.cashflow_score import CashFlowScore
from fundamental.scoring.growth_score import GrowthScore
from fundamental.scoring.efficiency_score import EfficiencyScore
from fundamental.scoring.financial_health_score import FinancialHealthScore
from fundamental.scoring.piotroski_score import PiotroskiScore
from fundamental.scoring.altman_score import AltmanScore
from fundamental.scoring.overall_score import OverallScore
from fundamental.scoring.beneish_score import BeneishScore
from fundamental.scoring.dupont_score import DupontScore
from fundamental.scoring.dcf_score import DCFScore
from fundamental.scoring.peter_lynch_score import PeterLynchScore
from fundamental.scoring.owner_earnings_score import OwnerEarningsScore
from fundamental.scoring.graham_score import GrahamScore
from fundamental.scoring.ev_multiple_score import EVMultipleScore
from fundamental.scoring.buffett_score import BuffettScore
from fundamental.scoring.magic_formula_score import MagicFormulaScore
from fundamental.scoring.economic_moat_score import EconomicMoatScore
from fundamental.scoring.dividend_quality_score import DividendQualityScore
from fundamental.scoring.shareholder_yield_score import ShareholderYieldScore
from fundamental.scoring.earnings_quality_score import EarningsQualityScore
from fundamental.scoring.roic_score import ROICScore
from fundamental.scoring.share_dilution_score import ShareDilutionScore
from fundamental.scoring.capital_allocation_score import CapitalAllocationScore
from fundamental.scoring.reinvestment_rate_score import ReinvestmentRateScore
from fundamental.scoring.capex_efficiency_score import CapexEfficiencyScore
from fundamental.scoring.cash_conversion_cycle_score import CashConversionCycleScore
from fundamental.scoring.revenue_stability_score import RevenueStabilityScore
from fundamental.scoring.earnings_stability_score import EarningsStabilityScore
from fundamental.scoring.eps_consistency_score import EPSConsistencyScore
from fundamental.scoring.margin_stability_score import MarginStabilityScore
from fundamental.scoring.debt_maturity_score import DebtMaturityScore
from fundamental.scoring.debt_service_coverage_score import DebtServiceCoverageScore
from fundamental.scoring.interest_rate_risk_score import InterestRateRiskScore
from fundamental.scoring.working_capital_quality_score import WorkingCapitalQualityScore
from fundamental.scoring.insider_ownership_score import InsiderOwnershipScore
from fundamental.scoring.institutional_ownership_score import InstitutionalOwnershipScore
from fundamental.scoring.insider_trading_score import InsiderTradingScore
from fundamental.scoring.management_quality_score import ManagementQualityScore
from fundamental.scoring.pricing_power_score import PricingPowerScore
from fundamental.scoring.market_leadership_score import MarketLeadershipScore
from fundamental.scoring.brand_strength_score import BrandStrengthScore
from fundamental.scoring.rd_efficiency_score import RDEfficiencyScore
from fundamental.scoring.residual_income_score import ResidualIncomeScore
from fundamental.scoring.eva_score import EVAScore
from fundamental.scoring.fcf_yield_score import FCFYieldScore
from fundamental.scoring.croic_score import CROICScore

class ScoringEngine:

    def __init__(self):
        self.profitability = ProfitabilityScore()
        self.growth = GrowthScore()
        self.liquidity = LiquidityScore()
        self.leverage = LeverageScore()
        self.valuation = ValuationScore()
        self.cashflow = CashFlowScore()
        self.efficiency = EfficiencyScore()
        self.financial_health = FinancialHealthScore()
        self.piotroski = PiotroskiScore()
        self.altman = AltmanScore()
        self.beneish = BeneishScore()
        self.overall = OverallScore()
        self.dupont = DupontScore()
        self.dcf = DCFScore()
        self.peter_lynch = PeterLynchScore()
        self.owner_earnings = OwnerEarningsScore()
        self.graham = GrahamScore()
        self.ev_multiple = EVMultipleScore()
        self.buffett = BuffettScore()
        self.magic_formula = MagicFormulaScore()
        self.economic_moat = EconomicMoatScore()
        self.dividend_quality = DividendQualityScore()
        self.shareholder_yield = ShareholderYieldScore()
        self.earnings_quality = EarningsQualityScore()
        self.roic = ROICScore()
        self.share_dilution = ShareDilutionScore()
        self.capital_allocation = CapitalAllocationScore()
        self.reinvestment_rate = ReinvestmentRateScore()
        self.capex_efficiency = CapexEfficiencyScore()
        self.cash_conversion_cycle = CashConversionCycleScore()
        self.revenue_stability = RevenueStabilityScore()
        self.earnings_stability = EarningsStabilityScore()
        self.eps_consistency = EPSConsistencyScore()
        self.margin_stability = MarginStabilityScore()
        self.debt_maturity = DebtMaturityScore()
        self.debt_service_coverage = DebtServiceCoverageScore()
        self.interest_rate_risk = InterestRateRiskScore()
        self.working_capital_quality = WorkingCapitalQualityScore()
        self.insider_ownership = InsiderOwnershipScore()
        self.institutional_ownership = InstitutionalOwnershipScore()
        self.insider_trading = InsiderTradingScore()
        self.management_quality = ManagementQualityScore()
        self.pricing_power = PricingPowerScore()
        self.market_leadership = MarketLeadershipScore()
        self.brand_strength = BrandStrengthScore()
        self.rd_efficiency = RDEfficiencyScore()
        self.residual_income = ResidualIncomeScore()
        self.eva = EVAScore()
        self.fcf_yield = FCFYieldScore()
        self.croic = CROICScore()

    def score(self, analysis):

        # -------------------------------------------------
        # Profitability
        # -------------------------------------------------

        profitability = analysis["profitability"]

        profitability_score = self.profitability.score(
            profitability["roe"],
            profitability["roa"],
            profitability["roce"],
            profitability["net_margin"],
        )

        # -------------------------------------------------
        # Growth
        # -------------------------------------------------

        growth = analysis["growth"]

        growth_score = self.growth.score(
            growth["revenue_growth"],
            growth["earnings_growth"],
            growth["eps_growth"],
        )

        # -------------------------------------------------
        # Liquidity
        # -------------------------------------------------

        liquidity = analysis["liquidity"]

        liquidity_score = self.liquidity.score(
            liquidity["current_ratio"],
            liquidity["quick_ratio"],
            liquidity["cash_ratio"],
        )

        # -------------------------------------------------
        # Leverage
        # -------------------------------------------------

        leverage = analysis["leverage"]

        leverage_score = self.leverage.score(
            leverage["debt_to_equity"],
            leverage["debt_to_assets"],
            leverage["equity_ratio"],
        )

        # -------------------------------------------------
        # Valuation
        # -------------------------------------------------

        valuation = analysis["valuation"]

        valuation_score = self.valuation.score(
            valuation["pe_ratio"],
            valuation["pb_ratio"],
            valuation["ps_ratio"],
            valuation["ev_to_ebitda"],
            valuation["peg_ratio"],
        )

        # -------------------------------------------------
        # Cash Flow
        # -------------------------------------------------

        cashflow = analysis["cashflow"]

        cashflow_score = self.cashflow.score(
            cashflow["operating_cash_flow"],
            cashflow["free_cash_flow"],
            cashflow["cashflow_growth"],
        )

        # -------------------------------------------------
        # Efficiency
        # -------------------------------------------------

        efficiency = analysis["efficiency"]

        efficiency_score = self.efficiency.score(
            efficiency["asset_turnover"],
            efficiency["inventory_turnover"],
            efficiency["receivables_turnover"],
            efficiency["working_capital_turnover"],
        )

        # -------------------------------------------------
        # Financial Health
        # -------------------------------------------------

        financial_health = analysis["financial_health"]

        financial_health_score = self.financial_health.score(
            financial_health["interest_coverage"],
            financial_health["debt_to_ebitda"],
            financial_health["financial_leverage"],
        )

        # -------------------------------------------------
        # Piotroski
        # -------------------------------------------------

        piotroski = analysis["piotroski"]

        piotroski_score = self.piotroski.score(
            piotroski["score"],
        )

        # -------------------------------------------------
        # Altman
        # -------------------------------------------------

        altman = analysis["altman"]

        altman_score = self.altman.score(
            altman["z_score"],
        )

        # -------------------------------------------------
        # Beneish
        # -------------------------------------------------

        beneish = analysis["beneish"]

        beneish_score = self.beneish.score(
            beneish["m_score"],
        )

        # -------------------------------------------------
        # DuPont
        # -------------------------------------------------

        dupont = analysis["dupont"]

        dupont_score = self.dupont.score(
            dupont["net_profit_margin"],
            dupont["asset_turnover"],
            dupont["equity_multiplier"],
            dupont["roe"],
        )

        # -------------------------------------------------
        # DCF
        # -------------------------------------------------

        dcf = analysis["dcf"]

        dcf_score = self.dcf.score(
            dcf["intrinsic_value"],
            dcf["current_price"],
            dcf["margin_of_safety"],
        )

        # -------------------------------------------------
        # Peter Lynch
        # -------------------------------------------------

        peter_lynch = analysis["peter_lynch"]

        peter_lynch_score = self.peter_lynch.score(
            peter_lynch["upside"],
        )

        # -------------------------------------------------
        # Owner Earnings
        # -------------------------------------------------

        owner_earnings = analysis["owner_earnings"]

        owner_earnings_score = self.owner_earnings.score(
            owner_earnings["owner_earnings_yield"],
        )

        # -------------------------------------------------
        # Benjamin Graham
        # -------------------------------------------------

        graham = analysis["graham"]

        graham_score = self.graham.score(
            graham["upside"],
        )

        # -------------------------------------------------
        # EV Multiple
        # -------------------------------------------------

        ev_multiple = analysis["ev_multiple"]

        ev_multiple_score = self.ev_multiple.score(
            ev_multiple["ev_to_ebitda"],
        )

        # -------------------------------------------------
        # Buffett
        # -------------------------------------------------

        buffett = analysis["buffett"]

        buffett_score = self.buffett.score(
            buffett["score"],
        )

        # -------------------------------------------------
        # Magic Formula
        # -------------------------------------------------

        magic_formula = analysis["magic_formula"]

        magic_formula_score = self.magic_formula.score(
            magic_formula["earnings_yield"],
            magic_formula["return_on_capital"],
        )

        # -------------------------------------------------
        # Economic Moat
        # -------------------------------------------------

        economic_moat = analysis["economic_moat"]

        economic_moat_score = self.economic_moat.score(
            economic_moat["score"],
        )

        # -------------------------------------------------
        # Dividend Quality
        # -------------------------------------------------

        dividend_quality = analysis["dividend_quality"]

        dividend_quality_score = self.dividend_quality.score(
            dividend_quality["score"],
        )

        # -------------------------------------------------
        # Shareholder Yield
        # -------------------------------------------------

        shareholder_yield = analysis["shareholder_yield"]

        shareholder_yield_score = self.shareholder_yield.score(
            shareholder_yield["score"],
        )

        # -------------------------------------------------
        # Earnings Quality
        # -------------------------------------------------

        earnings_quality = analysis["earnings_quality"]

        earnings_quality_score = self.earnings_quality.score(
            earnings_quality["score"],
        )

        # -------------------------------------------------
        # ROIC
        # -------------------------------------------------

        roic = analysis["roic"]

        roic_score = self.roic.score(
            roic["score"],
        )

        # -------------------------------------------------
        # Share Dilution
        # -------------------------------------------------

        share_dilution = analysis["share_dilution"]

        share_dilution_score = self.share_dilution.score(
            share_dilution["score"],
        )

        # -------------------------------------------------
        # Capital Allocation
        # -------------------------------------------------

        capital_allocation = analysis["capital_allocation"]

        capital_allocation_score = self.capital_allocation.score(
            capital_allocation["score"],
        )

        # -------------------------------------------------
        # Reinvestment Rate
        # -------------------------------------------------

        reinvestment_rate = analysis["reinvestment_rate"]

        reinvestment_rate_score = self.reinvestment_rate.score(
            reinvestment_rate["score"],
        )

        # -------------------------------------------------
        # Capital Expenditure Efficiency
        # -------------------------------------------------

        capex_efficiency = analysis["capex_efficiency"]

        capex_efficiency_score = self.capex_efficiency.score(
            capex_efficiency["score"],
        )

        # -------------------------------------------------
        # Cash Conversion Cycle
        # -------------------------------------------------

        cash_conversion_cycle = analysis["cash_conversion_cycle"]

        cash_conversion_cycle_score = self.cash_conversion_cycle.score(
            cash_conversion_cycle["score"],
        )

        # -------------------------------------------------
        # Revenue Stability
        # -------------------------------------------------

        revenue_stability = analysis["revenue_stability"]

        revenue_stability_score = self.revenue_stability.score(
            revenue_stability["score"],
        )

        # -------------------------------------------------
        # Earnings Stability
        # -------------------------------------------------

        earnings_stability = analysis["earnings_stability"]

        earnings_stability_score = self.earnings_stability.score(
            earnings_stability["score"],
        )

        # -------------------------------------------------
        # EPS Consistency
        # -------------------------------------------------

        eps_consistency = analysis["eps_consistency"]

        eps_consistency_score = self.eps_consistency.score(
            eps_consistency["score"],
        )

        # -------------------------------------------------
        # Margin Stability
        # -------------------------------------------------

        margin_stability = analysis["margin_stability"]

        margin_stability_score = self.margin_stability.score(
            margin_stability["score"],
        )

        # -------------------------------------------------
        # Debt Maturity
        # -------------------------------------------------

        debt_maturity = analysis["debt_maturity"]

        debt_maturity_score = self.debt_maturity.score(
            debt_maturity["score"],
        )

        # -------------------------------------------------
        # Debt Service Coverage
        # -------------------------------------------------

        debt_service_coverage = analysis["debt_service_coverage"]

        debt_service_coverage_score = (
            self.debt_service_coverage.score(
                debt_service_coverage["score"],
            )
        )

        # -------------------------------------------------
        # Interest Rate Risk
        # -------------------------------------------------

        interest_rate_risk = analysis["interest_rate_risk"]

        interest_rate_risk_score = self.interest_rate_risk.score(
            interest_rate_risk["score"],
        )

        # -------------------------------------------------
        # Working Capital Quality
        # -------------------------------------------------

        working_capital_quality = analysis[
            "working_capital_quality"
        ]

        working_capital_quality_score = (
            self.working_capital_quality.score(
                working_capital_quality["score"],
            )
        )

        # -------------------------------------------------
        # Insider Ownership
        # -------------------------------------------------

        insider_ownership = analysis["insider_ownership"]

        insider_ownership_score = (
            self.insider_ownership.score(
                insider_ownership["score"],
            )
        )

        # -------------------------------------------------
        # Institutional Ownership
        # -------------------------------------------------

        institutional_ownership = analysis[
            "institutional_ownership"
        ]

        institutional_ownership_score = (
            self.institutional_ownership.score(
                institutional_ownership["score"],
            )
        )

        # -------------------------------------------------
        # Insider Trading
        # -------------------------------------------------

        insider_trading = analysis[
            "insider_trading"
        ]

        insider_trading_score = (
            self.insider_trading.score(
                insider_trading["score"],
            )
        )

        # -------------------------------------------------
        # Management Quality
        # -------------------------------------------------

        management_quality = analysis[
            "management_quality"
        ]

        management_quality_score = (
            self.management_quality.score(
                management_quality["score"],
            )
        )

        # -------------------------------------------------
        # Pricing Power
        # -------------------------------------------------

        pricing_power = analysis[
            "pricing_power"
        ]

        pricing_power_score = (
            self.pricing_power.score(
                pricing_power["score"],
            )
        )

        # -------------------------------------------------
        # Market Leadership
        # -------------------------------------------------

        market_leadership = analysis[
            "market_leadership"
        ]

        market_leadership_score = (
            self.market_leadership.score(
                market_leadership["score"],
            )
        )

        # -------------------------------------------------
        # Brand Strength
        # -------------------------------------------------

        brand_strength = analysis[
            "brand_strength"
        ]

        brand_strength_score = (
            self.brand_strength.score(
                brand_strength["score"],
            )
        )

        # -------------------------------------------------
        # R&D Efficiency
        # -------------------------------------------------

        rd_efficiency = analysis[
            "rd_efficiency"
        ]

        rd_efficiency_score = (
            self.rd_efficiency.score(
                rd_efficiency["score"],
            )
        )

        # -------------------------------------------------
        # Residual Income Valuation
        # -------------------------------------------------

        residual_income = analysis[
            "residual_income"
        ]

        residual_income_score = (
            self.residual_income.score(
                residual_income["valuation"],
            )
        )

        # -------------------------------------------------
        # Economic Value Added (EVA)
        # -------------------------------------------------

        eva = analysis[
            "eva"
        ]

        eva_score = (
            self.eva.score(
                eva["quality"],
            )
        )

        # -------------------------------------------------
        # Free Cash Flow Yield
        # -------------------------------------------------

        fcf_yield = analysis[
            "fcf_yield"
        ]

        fcf_yield_score = (
            self.fcf_yield.score(
                fcf_yield["score"],
            )
        )

        # -------------------------------------------------
        # CROIC
        # -------------------------------------------------

        croic = analysis[
            "croic"
        ]

        croic_score = (
            self.croic.score(
                croic["score"],
            )
        )

        # -------------------------------------------------
        # Overall
        # -------------------------------------------------

        overall = self.overall.calculate(
            profitability_score,
            growth_score,
            liquidity_score,
            leverage_score,
            valuation_score,
            cashflow_score,
            efficiency_score,
            financial_health_score,
            piotroski_score,
            altman_score,
            beneish_score,
            dupont_score,
            dcf_score,
            peter_lynch_score,
            owner_earnings_score,
            graham_score,
            ev_multiple_score,
            buffett_score,
            magic_formula_score,
            economic_moat_score,
            dividend_quality_score,
            shareholder_yield_score,
            earnings_quality_score,
            roic_score,
            share_dilution_score,
            capital_allocation_score,
            reinvestment_rate_score,
            capex_efficiency_score,
            cash_conversion_cycle_score,
            revenue_stability_score,
            earnings_stability_score,
            eps_consistency_score,
            margin_stability_score,
            debt_maturity_score,
            debt_service_coverage_score,
            interest_rate_risk_score,
            working_capital_quality_score,
            insider_ownership_score,
            institutional_ownership_score,
            insider_trading_score,
            management_quality_score,
            pricing_power_score,
            market_leadership_score,
            brand_strength_score,
            rd_efficiency_score,
            residual_income_score,
            eva_score,
            fcf_yield_score,
            croic_score,
        )

        return {
            "profitability": profitability_score,
            "growth": growth_score,
            "liquidity": liquidity_score,
            "leverage": leverage_score,
            "valuation": valuation_score,
            "cashflow": cashflow_score,
            "efficiency": efficiency_score,
            "financial_health": financial_health_score,
            "piotroski": piotroski_score,
            "altman": altman_score,
            "beneish": beneish_score,
            "dupont": dupont_score,
            "dcf": dcf_score,
            "peter_lynch": peter_lynch_score,
            "owner_earnings": owner_earnings_score,
            "graham": graham_score,
            "ev_multiple": ev_multiple_score,
            "buffett": buffett_score,
            "magic_formula": magic_formula_score,
            "economic_moat": economic_moat_score,
            "dividend_quality": dividend_quality_score,
            "shareholder_yield": shareholder_yield_score,
            "earnings_quality": earnings_quality_score,
            "roic": roic_score,
            "share_dilution": share_dilution_score,
            "capital_allocation": capital_allocation_score,
            "reinvestment_rate": reinvestment_rate_score,
            "capex_efficiency": capex_efficiency_score,
            "cash_conversion_cycle": cash_conversion_cycle_score,
            "revenue_stability": revenue_stability_score,
            "earnings_stability": earnings_stability_score,
            "eps_consistency": eps_consistency_score,
            "margin_stability": margin_stability_score,
            "debt_maturity": debt_maturity_score,
            "debt_service_coverage": debt_service_coverage_score,
            "interest_rate_risk": interest_rate_risk_score,
            "working_capital_quality": working_capital_quality_score,
            "insider_ownership": insider_ownership_score,
            "institutional_ownership": institutional_ownership_score,
            "insider_trading": insider_trading_score,
            "management_quality": management_quality_score,
            "pricing_power": pricing_power_score,
            "market_leadership": market_leadership_score,
            "brand_strength": brand_strength_score,
            "rd_efficiency": rd_efficiency_score,
            "residual_income": residual_income_score,
            "eva": eva_score,
            "fcf_yield": fcf_yield_score,
            "croic": croic_score,
            "overall": overall,
        }