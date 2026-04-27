from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from app.core.database import Base

class Analysis(Base):
    __tablename__ = "analysis"

    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    domain = Column(String)
    score = Column(Float)
    matched_skills = Column(String(500))
    missing_skills = Column(String(500))

    selected = Column(Boolean, default=False)
    selection_reason = Column(String)         