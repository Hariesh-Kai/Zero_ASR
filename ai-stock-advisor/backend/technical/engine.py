from technical.collector import TechnicalCollector
from technical.mapper import TechnicalMapper

from technical.trend_analyzer import TrendAnalyzer
from technical.momentum_analyzer import MomentumAnalyzer
from technical.volume_analyzer import VolumeAnalyzer
from technical.volatility_analyzer import VolatilityAnalyzer

from technical.technical_scoring import TechnicalScoring
from technical.technical_recommendation import TechnicalRecommendation
from technical.technical_report import TechnicalReport


class TechnicalEngine:
    """
    Complete Technical Analysis Engine.
    """

    def __init__(self):

        self.collector = TechnicalCollector()

        self.mapper = TechnicalMapper()

        self.trend = TrendAnalyzer()

        self.momentum = MomentumAnalyzer()

        self.volume = VolumeAnalyzer()

        self.volatility = VolatilityAnalyzer()

        self.scoring = TechnicalScoring()

        self.recommendation = TechnicalRecommendation()

        self.report = TechnicalReport()

    def analyze(
        self,
        ticker: str,
    ):

        df = self.collector.collect(
            ticker
        )

        mapped = self.mapper.map(
            df
        )

        analysis = {

            "trend":
                self.trend.analyze(
                    mapped
                ),

            "momentum":
                self.momentum.analyze(
                    mapped
                ),

            "volume":
                self.volume.analyze(
                    mapped
                ),

            "volatility":
                self.volatility.analyze(
                    mapped
                ),
        }

        scores = self.scoring.score(
            analysis
        )

        recommendation = (
            self.recommendation.recommend(
                scores["technical_score"]
            )
        )

        return self.report.build(

            ticker,

            analysis,

            scores,

            recommendation,

        )