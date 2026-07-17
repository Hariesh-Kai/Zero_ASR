from fastapi import APIRouter

from technical.engine import TechnicalEngine

from models.technical import TechnicalResponse

router = APIRouter()

engine = TechnicalEngine()


@router.get(
    "/{ticker}",
    response_model=TechnicalResponse,
)
def analyze_technical(ticker: str):

    return engine.analyze(
        ticker.upper()
    )