from fundamental.engine import FundamentalEngine
from technical.engine import TechnicalEngine
from news.engine import NewsEngine
from advisor.summary import AdvisorSummary
from advisor.weighting import WeightingEngine
from advisor.decision import DecisionEngine
from advisor.confidence import ConfidenceEngine
from advisor.risk import RiskEngine
from advisor.report import AdvisorReport
from valuation.engine import ValuationEngine
from pprint import pprint


class AdvisorEngine:
    """
    Complete AI Stock Advisor Engine.

    This engine combines:
        • Fundamental Analysis
        • Technical Analysis
        • News Analysis

    into one final investment report.
    """

    def __init__(self):

        self.fundamental = FundamentalEngine()

        self.technical = TechnicalEngine()

        self.news = NewsEngine()

        self.valuation = ValuationEngine()

    def analyze(
        self,
        ticker: str,
    ):

        # ------------------------------------
        # Individual Engines
        # ------------------------------------

        fundamental = self.fundamental.analyze(
            ticker
        )

        technical = self.technical.analyze(
            ticker
        )

        news = self.news.analyze(
            ticker
        )

        valuation = self.valuation.analyze(
            ticker
        )

        # ------------------------------------
        # Advisor Engines
        # ------------------------------------

        weighting = WeightingEngine.calculate(

            fundamental,

            technical,

            news,

            valuation,

        )

        decision = DecisionEngine.decide(

            weighting["advisor_score"]

        )

        confidence = ConfidenceEngine.calculate(

            fundamental,

            technical,

            news,

            valuation,

        )

        risk = RiskEngine.assess(

            fundamental,

            technical,

            news,

            valuation,

        )

        summary = AdvisorSummary.generate(

            company=fundamental["company"]["name"],

            advisor_score=weighting["advisor_score"],

            recommendation=decision,

            fundamental=fundamental,

            technical=technical,

            news=news,

            valuation=valuation,

            risk=risk,

        )


        return AdvisorReport.build(

            ticker,

            weighting,

            decision,

            confidence,

            risk,

            summary,

            fundamental,

            technical,

            news,

            valuation,

        )