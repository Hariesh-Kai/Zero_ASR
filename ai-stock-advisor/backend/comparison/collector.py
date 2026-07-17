from fundamental.engine import FundamentalEngine
from technical.engine import TechnicalEngine
from news.engine import NewsEngine
from valuation.engine import ValuationEngine
from advisor.engine import AdvisorEngine


class ComparisonCollector:
    """
    Collects all analysis required to compare
    two companies.
    """

    def __init__(self):

        self.fundamental = FundamentalEngine()

        self.technical = TechnicalEngine()

        self.news = NewsEngine()

        self.valuation = ValuationEngine()

        self.advisor = AdvisorEngine()

    def collect(

        self,

        ticker_one: str,

        ticker_two: str,

    ):

        return {

            ticker_one.upper(): {

                "fundamental": self.fundamental.analyze(
                    ticker_one,
                ),

                "technical": self.technical.analyze(
                    ticker_one,
                ),

                "news": self.news.analyze(
                    ticker_one,
                ),

                "valuation": self.valuation.analyze(
                    ticker_one,
                ),

                "advisor": self.advisor.analyze(
                    ticker_one,
                ),

            },

            ticker_two.upper(): {

                "fundamental": self.fundamental.analyze(
                    ticker_two,
                ),

                "technical": self.technical.analyze(
                    ticker_two,
                ),

                "news": self.news.analyze(
                    ticker_two,
                ),

                "valuation": self.valuation.analyze(
                    ticker_two,
                ),

                "advisor": self.advisor.analyze(
                    ticker_two,
                ),

            },

        }