from pydantic import BaseModel
from typing import Any, Dict


class FundamentalResponse(BaseModel):

    engine: str

    version: str

    generated_at: str

    ticker: str

    company: Dict[str, Any]

    analysis: Dict[str, Any]

    scores: Dict[str, Any]

    recommendation: Dict[str, Any]

    ai_summary: Any