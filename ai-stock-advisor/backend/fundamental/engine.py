from fundamental.collector import FundamentalCollector
from fundamental.scoring_engine import ScoringEngine
from fundamental.recommendation import RecommendationEngine
from fundamental.report import FundamentalReport
from ai.summary import AISummary

class FundamentalEngine:

    def __init__(self):
        self.collector = FundamentalCollector()
        self.scoring = ScoringEngine()
        self.recommendation = RecommendationEngine()
        self.report = FundamentalReport()
        self.ai = AISummary()

    def analyze(self, ticker: str):

        company_data = self.collector.collect(ticker)


        scores = self.scoring.score(
            company_data["analysis"]
        )

        recommendation = self.recommendation.recommend(
            scores["overall"]["overall_score"]
        )

        ai_summary = self.ai.generate(
            company_data["analysis"],
            scores,
            recommendation,
        )

        return self.report.build(
            company_data["company"],
            company_data["analysis"],
            scores,
            recommendation,
            ai_summary,
        )