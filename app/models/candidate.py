from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    email = Column(String(255), unique=True, index=True)
    phone = Column(String, nullable=True)
    resume_file = Column(String, nullable=True)