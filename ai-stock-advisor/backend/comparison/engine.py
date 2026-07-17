from comparison.collector import ComparisonCollector
from comparison.metrics import ComparisonMetrics
from comparison.scoring import ComparisonScoring
from comparison.winner import ComparisonWinner
from comparison.summary import ComparisonSummary
from comparison.report import ComparisonReport


class ComparisonEngine:
    """
    Complete Comparison Engine.

    Compares two companies using:
        • Fundamental Analysis
        • Technical Analysis
        • News Analysis
        • Valuation Analysis
        • AI Advisor
    """

    def __init__(self):

        self.collector = ComparisonCollector()

        self.metrics = ComparisonMetrics()

        self.scoring = ComparisonScoring()

        self.winner = ComparisonWinner()

        self.summary = ComparisonSummary()

        self.report = ComparisonReport()

    def compare(

        self,

        ticker_one: str,

        ticker_two: str,

    ):

        # -----------------------------------
        # Collect Analysis
        # -----------------------------------

        data = self.collector.collect(

            ticker_one,

            ticker_two,

        )

        company_one = self.metrics.extract(

            data[ticker_one.upper()]

        )

        company_two = self.metrics.extract(

            data[ticker_two.upper()]

        )

        # -----------------------------------
        # Compare
        # -----------------------------------

        comparison = self.scoring.compare(

            company_one,

            company_two,

        )

        # -----------------------------------
        # Winner
        # -----------------------------------

        winner = self.winner.decide(

            comparison["scoreboard"]

        )

        # -----------------------------------
        # Summary
        # -----------------------------------

        summary = self.summary.generate(

            company_one,

            company_two,

            comparison,

            winner,

        )

        # -----------------------------------
        # Final Report
        # -----------------------------------

        return self.report.build(

            ticker_one=ticker_one.upper(),

            ticker_two=ticker_two.upper(),

            company_one=company_one,

            company_two=company_two,

            comparison=comparison,

            winner=winner,

            summary=summary,

        )