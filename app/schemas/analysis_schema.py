from pydantic import BaseModel
from typing import List


class DomainPrediction(BaseModel):
    domain: str
    score: float


class AnalysisResult(BaseModel):
    predicted_domain: str
    confidence: str
    match_score: float
    similarity_score: float
    skill_score: float
    missing_skills: List[str]
    reason: str
    top_predictions: List[DomainPrediction]