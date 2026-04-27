# models/candidate.py

from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20))
    score = Column(Integer)
    domain = Column(String(255))
    missing_skills = Column(String)
    selected = Column(Boolean, default=False)