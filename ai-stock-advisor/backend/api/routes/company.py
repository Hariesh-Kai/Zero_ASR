from fastapi import APIRouter

from fundamental.engine import FundamentalEngine

from models.fundamental import FundamentalResponse

router = APIRouter()

engine = FundamentalEngine()


@router.get(
    "/{ticker}",
    response_model=FundamentalResponse,
)
def analyze_company(ticker: str):

    return engine.analyze(
        ticker.upper()
    )