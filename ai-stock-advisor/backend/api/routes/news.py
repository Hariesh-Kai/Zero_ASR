from fastapi import APIRouter

from news.engine import NewsEngine

from models.news import NewsResponse

router = APIRouter()

engine = NewsEngine()


@router.get(
    "/{ticker}",
    response_model=NewsResponse,
)
def analyze_news(ticker: str):

    return engine.analyze(
        ticker.upper()
    )