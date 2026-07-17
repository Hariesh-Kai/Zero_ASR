from pydantic import BaseModel
from typing import Any, Dict


class TechnicalResponse(BaseModel):

    engine: str

    version: str

    generated_at: str

    ticker: str

    analysis: Dict[str, Any]

    scores: Dict[str, Any]

    recommendation: Dict[str, Any]