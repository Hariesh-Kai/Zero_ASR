from typing import Any, Dict

from data.company_data import CompanyData

from fundamental.analyzer import FundamentalAnalyzer
from fundamental.growth_analyzer import GrowthAnalyzer
from fundamental.valuation_analyzer import ValuationAnalyzer
from fundamental.cashflow_analyzer import CashFlowAnalyzer
from fundamental.efficiency_analyzer import EfficiencyAnalyzer
from fundamental.extractor import FinancialExtractor
from fundamental.financial_health_analyzer import FinancialHealthAnalyzer
from fundamental.historical_analyzer import HistoricalAnalyzer
from fundamental.piotroski import PiotroskiFScore
from fundamental.altman_analyzer import AltmanAnalyzer
from fundamental.beneish_analyzer import BeneishAnalyzer
from fundamental.dupont_analyzer import DupontAnalyzer
from fundamental.dcf_analyzer import DCFAnalyzer
from fundamental.peter_lynch_analyzer import PeterLynchAnalyzer
from fundamental.owner_earnings_analyzer import OwnerEarningsAnalyzer
from fundamental.graham_analyzer import GrahamAnalyzer
from fundamental.ev_multiple_analyzer import EVMultipleAnalyzer
from fundamental.buffett_analyzer import BuffettAnalyzer
from fundamental.magic_formula_analyzer import MagicFormulaAnalyzer
from fundamental.economic_moat_analyzer import EconomicMoatAnalyzer
from fundamental.dividend_quality_analyzer import DividendQualityAnalyzer
from fundamental.shareholder_yield_analyzer import ShareholderYieldAnalyzer
from fundamental.earnings_quality_analyzer import EarningsQualityAnalyzer
from fundamental.roic_analyzer import ROICAnalyzer
from fundamental.share_dilution_analyzer import ShareDilutionAnalyzer
from fundamental.capital_allocation_analyzer import CapitalAllocationAnalyzer
from fundamental.reinvestment_rate_analyzer import ReinvestmentRateAnalyzer
from fundamental.capex_efficiency_analyzer import CapexEfficiencyAnalyzer
from fundamental.cash_conversion_cycle_analyzer import CashConversionCycleAnalyzer
from fundamental.revenue_stability_analyzer import RevenueStabilityAnalyzer
from fundamental.earnings_stability_analyzer import EarningsStabilityAnalyzer
from fundamental.eps_consistency_analyzer import EPSConsistencyAnalyzer
from fundamental.margin_stability_analyzer import MarginStabilityAnalyzer
from fundamental.debt_maturity_analyzer import DebtMaturityAnalyzer
from fundamental.debt_service_coverage_analyzer import DebtServiceCoverageAnalyzer
from fundamental.interest_rate_risk_analyzer import InterestRateRiskAnalyzer
from fundamental.working_capital_quality_analyzer import WorkingCapitalQualityAnalyzer
from fundamental.insider_ownership_analyzer import InsiderOwnershipAnalyzer
from fundamental.institutional_ownership_analyzer import InstitutionalOwnershipAnalyzer
from fundamental.insider_trading_analyzer import InsiderTradingAnalyzer
from fundamental.management_quality_analyzer import ManagementQualityAnalyzer
from fundamental.pricing_power_analyzer import PricingPowerAnalyzer
from fundamental.market_leadership_analyzer import MarketLeadershipAnalyzer
from fundamental.brand_strength_analyzer import BrandStrengthAnalyzer
from fundamental.rd_efficiency_analyzer import RDEfficiencyAnalyzer
from fundamental.residual_income_analyzer import ResidualIncomeAnalyzer
from fundamental.eva_analyzer import EVAAnalyzer
from fundamental.fcf_yield_analyzer import FCFYieldAnalyzer
from fundamental.croic_analyzer import CROICAnalyzer

class FundamentalCollector:
    """
    Collects and standardizes all company data required
    for the Fundamental Analysis Engine.
    """

    def __init__(self):
        self.company_data = CompanyData()
        self.analyzer = FundamentalAnalyzer()
        self.growth = GrowthAnalyzer()
        self.valuation = ValuationAnalyzer()
        self.cashflow = CashFlowAnalyzer()
        self.efficiency = EfficiencyAnalyzer()
        self.financial_health = FinancialHealthAnalyzer()
        self.history = HistoricalAnalyzer()
        self.piotroski = PiotroskiFScore()
        self.altman = AltmanAnalyzer()
        self.beneish = BeneishAnalyzer()
        self.dupont = DupontAnalyzer()
        self.dcf = DCFAnalyzer()
        self.peter_lynch = PeterLynchAnalyzer()
        self.owner_earnings = OwnerEarningsAnalyzer()
        self.graham = GrahamAnalyzer()
        self.ev_multiple = EVMultipleAnalyzer()
        self.buffett = BuffettAnalyzer()
        self.magic_formula = MagicFormulaAnalyzer()
        self.economic_moat = EconomicMoatAnalyzer()
        self.dividend_quality = DividendQualityAnalyzer()
        self.shareholder_yield = ShareholderYieldAnalyzer()
        self.earnings_quality = EarningsQualityAnalyzer()
        self.roic = ROICAnalyzer()
        self.share_dilution = ShareDilutionAnalyzer()
        self.capital_allocation = CapitalAllocationAnalyzer()
        self.reinvestment_rate = ReinvestmentRateAnalyzer()
        self.capex_efficiency = CapexEfficiencyAnalyzer()
        self.cash_conversion_cycle = CashConversionCycleAnalyzer()
        self.revenue_stability = RevenueStabilityAnalyzer()
        self.earnings_stability = EarningsStabilityAnalyzer()
        self.eps_consistency = EPSConsistencyAnalyzer()
        self.margin_stability = MarginStabilityAnalyzer()
        self.debt_maturity = DebtMaturityAnalyzer()
        self.debt_service_coverage = DebtServiceCoverageAnalyzer()
        self.interest_rate_risk = InterestRateRiskAnalyzer()
        self.working_capital_quality = WorkingCapitalQualityAnalyzer()
        self.insider_ownership = InsiderOwnershipAnalyzer()
        self.institutional_ownership = InstitutionalOwnershipAnalyzer()
        self.insider_trading = InsiderTradingAnalyzer()
        self.management_quality = ManagementQualityAnalyzer()
        self.pricing_power = PricingPowerAnalyzer()
        self.market_leadership = MarketLeadershipAnalyzer()
        self.brand_strength = BrandStrengthAnalyzer()
        self.rd_efficiency = RDEfficiencyAnalyzer()
        self.residual_income = ResidualIncomeAnalyzer()
        self.eva = EVAAnalyzer()
        self.fcf_yield = FCFYieldAnalyzer()
        self.croic = CROICAnalyzer()

    def collect(self, ticker: str) -> Dict[str, Any]:
        """
        Returns standardized company data.
        """

        company_data = self.company_data.load(
            ticker
        )
        print(company_data["profile"])

        financial_data = {
            "financial_statements": company_data["financial_statements"],
            "quarterly_financials": company_data["quarterly_financials"],
        }

        extracted = FinancialExtractor.extract(
            financial_data,
            company_data["profile"],
        )

        mapped = extracted["mapped"]
        previous_mapped = extracted["previous_mapped"]

        # ----------------------------------------------------
        # Core Fundamental Analysis
        # ----------------------------------------------------

        analysis = self.analyzer.analyze(extracted)

        # ----------------------------------------------------
        # Growth
        # ----------------------------------------------------

        growth = self.growth.analyze(
            extracted["income_statement"],
            extracted["cash_flow"],
        )

        analysis["growth"] = growth

        # ----------------------------------------------------
        # Valuation
        # ----------------------------------------------------

        valuation = self.valuation.analyze(
            company_data["profile"],
            mapped,
            growth,
        )

        analysis["valuation"] = valuation

        # ----------------------------------------------------
        # Cash Flow
        # ----------------------------------------------------

        cashflow = self.cashflow.analyze(
            mapped,
            growth,
        )

        analysis["cashflow"] = cashflow

        # ----------------------------------------------------
        # Financial Health
        # ----------------------------------------------------

        financial_health = self.financial_health.analyze(
            mapped,
        )

        analysis["financial_health"] = financial_health

        # ----------------------------------------------------
        # Efficiency
        # ----------------------------------------------------

        efficiency = self.efficiency.analyze(
            mapped,
        )

        analysis["efficiency"] = efficiency

        # ----------------------------------------------------
        # Historical Analysis
        # ----------------------------------------------------

        current_history = self.history.analyze(
            mapped,
        )

        previous_history = self.history.analyze(
            previous_mapped,
        )

        analysis["history"] = {
            "current": current_history,
            "previous": previous_history,
        }

        # ----------------------------------------------------
        # Piotroski F-Score
        # ----------------------------------------------------

        piotroski = self.piotroski.calculate(
            current_history,
            previous_history,
        )

        analysis["piotroski"] = piotroski

        # ----------------------------------------------------
        # Altman Z-Score
        # ----------------------------------------------------

        altman = self.altman.analyze(
            mapped,
        )

        analysis["altman"] = altman

        # ----------------------------------------------------
        # Beneish M-Score
        # ----------------------------------------------------

        beneish = self.beneish.analyze(
            mapped,
            previous_mapped,
        )

        analysis["beneish"] = beneish

        # ----------------------------------------------------
        # DuPont Analysis
        # ----------------------------------------------------

        dupont = self.dupont.analyze(
            mapped,
        )

        analysis["dupont"] = dupont

        # ----------------------------------------------------
        # Discounted Cash Flow (DCF)
        # ----------------------------------------------------

        dcf = self.dcf.analyze(
            mapped,
            growth,
        )

        analysis["dcf"] = dcf

        # ----------------------------------------------------
        # Peter Lynch Fair Value
        # ----------------------------------------------------

        peter_lynch = self.peter_lynch.analyze(
            company_data["profile"],
            growth,
        )

        analysis["peter_lynch"] = peter_lynch

        # ----------------------------------------------------
        # Owner Earnings
        # ----------------------------------------------------

        owner_earnings = self.owner_earnings.analyze(
            mapped,
        )

        analysis["owner_earnings"] = owner_earnings

        # ----------------------------------------------------
        # Benjamin Graham Intrinsic Value
        # ----------------------------------------------------

        graham = self.graham.analyze(
            mapped,
            growth,
        )

        analysis["graham"] = graham

        # ----------------------------------------------------
        # EV Multiple Analysis
        # ----------------------------------------------------

        ev_multiple = self.ev_multiple.analyze(
            mapped,
        )

        analysis["ev_multiple"] = ev_multiple

        # ----------------------------------------------------
        # Buffett Analysis
        # ----------------------------------------------------

        buffett = self.buffett.analyze(
            mapped,
        )

        analysis["buffett"] = buffett

        # ----------------------------------------------------
        # Magic Formula Analysis
        # ----------------------------------------------------

        magic_formula = self.magic_formula.analyze(
            mapped,
        )

        analysis["magic_formula"] = magic_formula

        # ----------------------------------------------------
        # Economic Moat Analysis
        # ----------------------------------------------------

        economic_moat = self.economic_moat.analyze(
            analysis["profitability"],
            analysis["leverage"],
        )

        analysis["economic_moat"] = economic_moat

        # ----------------------------------------------------
        # Dividend Quality Analysis
        # ----------------------------------------------------

        dividend_quality = self.dividend_quality.analyze(
            company_data["profile"],
            mapped,
        )

        analysis["dividend_quality"] = dividend_quality

        # ----------------------------------------------------
        # Shareholder Yield Analysis
        # ----------------------------------------------------

        shareholder_yield = self.shareholder_yield.analyze(
            company_data["profile"],
            mapped,
            previous_mapped,
        )

        analysis["shareholder_yield"] = shareholder_yield

        # ----------------------------------------------------
        # Earnings Quality Analysis
        # ----------------------------------------------------

        earnings_quality = self.earnings_quality.analyze(
            mapped,
        )

        analysis["earnings_quality"] = earnings_quality

        # ----------------------------------------------------
        # ROIC Analysis
        # ----------------------------------------------------

        roic = self.roic.analyze(
            mapped,
        )

        analysis["roic"] = roic

        # ----------------------------------------------------
        # Share Dilution Analysis
        # ----------------------------------------------------

        share_dilution = self.share_dilution.analyze(
            mapped,
            previous_mapped,
        )

        analysis["share_dilution"] = share_dilution

        # ----------------------------------------------------
        # Capital Allocation Analysis
        # ----------------------------------------------------

        capital_allocation = self.capital_allocation.analyze(
            mapped,
        )

        analysis["capital_allocation"] = capital_allocation

        # ----------------------------------------------------
        # Reinvestment Rate Analysis
        # ----------------------------------------------------

        reinvestment_rate = self.reinvestment_rate.analyze(
            mapped,
        )

        analysis["reinvestment_rate"] = reinvestment_rate 

        # ----------------------------------------------------
        # Capital Expenditure Efficiency Analysis
        # ----------------------------------------------------

        capex_efficiency = self.capex_efficiency.analyze(
            mapped,
        )

        analysis["capex_efficiency"] = capex_efficiency 

        # ----------------------------------------------------
        # Cash Conversion Cycle Analysis
        # ----------------------------------------------------

        cash_conversion_cycle = self.cash_conversion_cycle.analyze(
            mapped,
        )

        analysis["cash_conversion_cycle"] = cash_conversion_cycle
        
        # ----------------------------------------------------
        # Revenue Stability Analysis
        # ----------------------------------------------------

        revenue_stability = self.revenue_stability.analyze(
            mapped,
            previous_mapped,
        )

        analysis["revenue_stability"] = revenue_stability

        # ----------------------------------------------------
        # Earnings Stability Analysis
        # ----------------------------------------------------

        earnings_stability = self.earnings_stability.analyze(
            mapped,
            previous_mapped,
        )

        analysis["earnings_stability"] = earnings_stability

        # ----------------------------------------------------
        # EPS Consistency Analysis
        # ----------------------------------------------------

        eps_consistency = self.eps_consistency.analyze(
            mapped,
            previous_mapped,
        )

        analysis["eps_consistency"] = eps_consistency

        # ----------------------------------------------------
        # Margin Stability Analysis
        # ----------------------------------------------------

        margin_stability = self.margin_stability.analyze(
            mapped,
            previous_mapped,
        )

        analysis["margin_stability"] = margin_stability

        # ----------------------------------------------------
        # Debt Maturity Analysis
        # ----------------------------------------------------

        debt_maturity = self.debt_maturity.analyze(
            mapped,
        )

        analysis["debt_maturity"] = debt_maturity

        # ----------------------------------------------------
        # Debt Service Coverage Analysis
        # ----------------------------------------------------

        debt_service_coverage = self.debt_service_coverage.analyze(
            mapped,
        )

        analysis["debt_service_coverage"] = debt_service_coverage

        # ----------------------------------------------------
        # Interest Rate Risk Analysis
        # ----------------------------------------------------

        interest_rate_risk = self.interest_rate_risk.analyze(
            mapped,
        )

        analysis["interest_rate_risk"] = interest_rate_risk
        
        # ----------------------------------------------------
        # Working Capital Quality Analysis
        # ----------------------------------------------------

        working_capital_quality = (
            self.working_capital_quality.analyze(
                mapped,
            )
        )

        analysis["working_capital_quality"] = (
            working_capital_quality
        )

        # ----------------------------------------------------
        # Insider Ownership Analysis
        # ----------------------------------------------------

        insider_ownership = self.insider_ownership.analyze(
            company_data["profile"],
        )

        analysis["insider_ownership"] = insider_ownership

        # ----------------------------------------------------
        # Institutional Ownership Analysis
        # ----------------------------------------------------

        institutional_ownership = (
            self.institutional_ownership.analyze(
                company_data["profile"],
            )
        )

        analysis["institutional_ownership"] = (
            institutional_ownership
        )

        # ----------------------------------------------------
        # Insider Trading Analysis
        # ----------------------------------------------------

        insider_trading = (
            self.insider_trading.analyze(
                company_data["profile"],
            )
        )

        analysis["insider_trading"] = (
            insider_trading
        )

        # ----------------------------------------------------
        # Management Quality Analysis
        # ----------------------------------------------------

        management_quality = (
            self.management_quality.analyze(
                mapped,
            )
        )

        analysis["management_quality"] = (
            management_quality
        )

        # ----------------------------------------------------
        # Pricing Power Analysis
        # ----------------------------------------------------

        pricing_power = (
            self.pricing_power.analyze(
                mapped,
            )
        )

        analysis["pricing_power"] = (
            pricing_power
        )

        # ----------------------------------------------------
        # Market Leadership Analysis
        # ----------------------------------------------------

        market_leadership = (
            self.market_leadership.analyze(
                mapped,
            )
        )

        analysis["market_leadership"] = (
            market_leadership
        )

        # ----------------------------------------------------
        # Brand Strength Analysis
        # ----------------------------------------------------

        brand_strength = (
            self.brand_strength.analyze(
                mapped,
            )
        )

        analysis["brand_strength"] = (
            brand_strength
        )

        # ----------------------------------------------------
        # R&D Efficiency Analysis
        # ----------------------------------------------------

        rd_efficiency = (
            self.rd_efficiency.analyze(
                mapped,
            )
        )

        analysis["rd_efficiency"] = (
            rd_efficiency
        )

        # ----------------------------------------------------
        # Residual Income Valuation
        # ----------------------------------------------------

        residual_income = (
            self.residual_income.analyze(
                mapped,
            )
        )

        analysis["residual_income"] = (
            residual_income
        )

        # ----------------------------------------------------
        # Economic Value Added (EVA)
        # ----------------------------------------------------

        eva = (
            self.eva.analyze(
                mapped,
            )
        )

        analysis["eva"] = (
            eva
        )

        # ----------------------------------------------------
        # Free Cash Flow Yield
        # ----------------------------------------------------

        fcf_yield = (
            self.fcf_yield.analyze(
                mapped,
            )
        )

        analysis["fcf_yield"] = (
            fcf_yield
        )

        # ----------------------------------------------------
        # CROIC Analysis
        # ----------------------------------------------------

        croic = (
            self.croic.analyze(
                mapped,
            )
        )

        analysis["croic"] = (
            croic
        )
                
        return {
            "company": company_data["profile"],
            "financials": extracted,
            "analysis": analysis,
        }