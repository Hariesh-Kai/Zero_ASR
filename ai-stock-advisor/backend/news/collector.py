from data.news_data import NewsData


class NewsCollector:
    """
    Collects company news.
    """

    def __init__(self):

        self.news = NewsData()

    def collect(
        self,
        ticker: str,
    ):

        return self.news.load(
            ticker
        )