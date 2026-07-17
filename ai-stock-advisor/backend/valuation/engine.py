from valuation.collector import ValuationCollector

from valuation.dcf.engine import ProfessionalDCF
from valuation.graham import GrahamModel
from valuation.peter_lynch import PeterLynchModel
from valuation.buffett import BuffettModel
from valuation.owner_earnings import OwnerEarningsModel
from valuation.ev_multiple import EVMultipleModel
from valuation.residual_income import ResidualIncomeModel
from valuation.magic_formula import MagicFormulaModel

from valuation.recommendation import ValuationRecommendation
from valuation.summary import ValuationSummary
from valuation.report import ValuationReport


class ValuationEngine:
    """
    Complete Valuation Engine.
    """

    def __init__(self):

        self.collector = ValuationCollector()

        self.dcf = ProfessionalDCF()

        self.graham = GrahamModel()

        self.peter_lynch = PeterLynchModel()

        self.buffett = BuffettModel()

        self.owner_earnings = OwnerEarningsModel()

        self.ev_multiple = EVMultipleModel()

        self.residual_income = ResidualIncomeModel()

        self.magic_formula = MagicFormulaModel()

        self.recommendation = ValuationRecommendation()

        self.summary = ValuationSummary()

        self.report = ValuationReport()

    def analyze(
        self,
        ticker: str,
    ):

        data = self.collector.collect(
            ticker
        )

        # valuation models will go here

        dcf = self.dcf.value(
            data["company"],
            data,
        )

        graham = self.graham.analyze(
            data
        )

        peter_lynch = self.peter_lynch.analyze(
            data
        )

        owner_earnings = self.owner_earnings.analyze(
            data
        )

        ev_multiple = self.ev_multiple.analyze(
            data
        )

        residual_income = self.residual_income.analyze(
            data
        )

        magic_formula = self.magic_formula.analyze(
            data
        )

        results = {

            "dcf": dcf,

            "graham": graham,

            "peter_lynch": peter_lynch,

            "owner_earnings": owner_earnings,

            "ev_multiple": ev_multiple,

            "residual_income":residual_income,

            "magic_formula":magic_formula,

        }

        recommendation = self.recommendation.recommend(
            results
        )

        summary = self.summary.generate(

            {

                "valuations": results,

                "recommendation": recommendation,

            }

        )

        return self.report.build(

            ticker,

            results,

            recommendation,

            summary,

        )