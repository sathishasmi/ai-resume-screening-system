from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base

class Analysis(Base):
    __tablename__ = "analysis"

    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer)

    domain = Column(String)
    score = Column(Float)

    matched_skills = Column(String)
    missing_skills = Column(String)

    selected = Column(String, default="No")
    selection_reason = Column(String)         