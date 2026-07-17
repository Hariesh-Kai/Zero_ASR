from fastapi import APIRouter

from financials.engine import FinancialEngine

router = APIRouter()

engine = FinancialEngine()


@router.get("/{ticker}")
def analyze_financials(ticker: str):

    return engine.analyze(
        ticker.upper()
    )