from historical.trends import TrendAnalyzer
from historical.growth import GrowthAnalyzer
from historical.quality import QualityAnalyzer


class HistoricalAnalyzer:
    """
    Performs complete historical financial analysis.
    """

    def __init__(self):

        self.trend = TrendAnalyzer()
        self.growth = GrowthAnalyzer()
        self.quality = QualityAnalyzer()

    def analyze(
        self,
        revenue,
        earnings,
        free_cash_flow,
        book_value,
        roe,
        roic,
    ):

        return {

            "trends": {

                "revenue":
                    self.trend.analyze(revenue),

                "earnings":
                    self.trend.analyze(earnings),

                "free_cash_flow":
                    self.trend.analyze(
                        free_cash_flow
                    ),

                "book_value":
                    self.trend.analyze(book_value),
            },

            "growth":

                self.growth.analyze(

                    revenue,

                    earnings,

                    free_cash_flow,

                    book_value,
                ),

            "quality":

                self.quality.analyze(

                    revenue,

                    earnings,

                    free_cash_flow,

                    roe,

                    roic,
                ),
        }