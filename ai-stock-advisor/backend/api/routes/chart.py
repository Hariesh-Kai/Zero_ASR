from fastapi import APIRouter

from services.chart_service import ChartService

router = APIRouter()

service = ChartService()


@router.get("/{ticker}")
def get_chart(
    ticker: str,
    period: str = "6mo",
):

    return service.get_chart(
        ticker.upper(),
        period,
    )