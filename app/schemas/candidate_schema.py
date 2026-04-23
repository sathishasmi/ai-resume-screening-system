from pydantic import BaseModel, EmailStr
from typing import Optional


class CandidateCreate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]


class CandidateResponse(BaseModel):
    id: int
    name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    resume_file: Optional[str]

    class Config:
        orm_mode = True