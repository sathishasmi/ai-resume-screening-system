# app/schemas/schema.py
from pydantic import BaseModel
from typing import List

class Result(BaseModel):
    name: str
    domain: str
    score: float
    skills: List[str]
    missing_skills: List[str]
    suitability: str