# models/candidate.py

from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20))
    resume_file = Column(String(255), nullable=False)

    # 🔥 NEW: link to job
    job_id = Column(Integer, ForeignKey("jobs.id"))