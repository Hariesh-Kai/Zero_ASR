from fastapi import APIRouter, HTTPException

from advisor.engine import AdvisorEngine

from models.advisor import AdvisorResponse

router = APIRouter()

engine = AdvisorEngine()


@router.get(
    "/{ticker}",
    response_model=AdvisorResponse,
)
def analyze_advisor(ticker: str):

    try:

        result = engine.analyze(
            ticker.upper()
        )

        return result

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )