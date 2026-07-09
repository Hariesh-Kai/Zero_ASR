from fastapi import APIRouter

from fundamental.engine import FundamentalEngine

router = APIRouter()

engine = FundamentalEngine()


@router.get("/{ticker}")
def analyze_company(ticker: str):

    return engine.analyze(ticker)