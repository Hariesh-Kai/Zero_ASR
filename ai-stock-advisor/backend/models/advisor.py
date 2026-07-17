from pydantic import BaseModel
from typing import Any, Dict


class RecommendationModel(BaseModel):

    advisor_score: float

    rating: str

    recommendation: str

    confidence: str


class ConfidenceModel(BaseModel):

    confidence_score: float

    confidence: str

    engine_scores: list[int]


class RiskModel(BaseModel):

    risk_score: float

    risk_level: str


class AdvisorResponse(BaseModel):

    engine: str

    version: str

    generated_at: str

    ticker: str

    advisor_score: float

    recommendation: RecommendationModel

    confidence: ConfidenceModel

    risk: RiskModel

    weighting: Dict[str, Any]

    engines: Dict[str, Any]