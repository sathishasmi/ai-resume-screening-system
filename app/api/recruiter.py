from fastapi import APIRouter
from app.core.database import SessionLocal
from app.models.candidate import Candidate
from app.models.analysis import Analysis

router = APIRouter()


# -----------------------------------
# Get all candidates
# -----------------------------------
@router.get("/recruiter/candidates")
def get_candidates():
    db = SessionLocal()

    data = db.query(Candidate, Analysis).join(
        Analysis, Candidate.id == Analysis.candidate_id
    ).all()

    db.close()

    return [
        {
            "id": a.id,
            "name": c.name,
            "email": c.email,
            "phone": c.phone,
            "score": a.score,
            "domain": a.domain,
            "missing_skills": a.missing_skills,
            "selected": a.selected,
            "selection_reason": a.selection_reason
        }
        for c, a in data
    ]


# -----------------------------------
# Select candidate
# -----------------------------------
from pydantic import BaseModel

class DecisionRequest(BaseModel):
    id: int
    action: str   # shortlist / reject
    reason: str

@router.post("/recruiter/decision")
def decide_candidate(data: DecisionRequest):
    db = SessionLocal()

    record = db.query(Analysis).filter(Analysis.id == data.id).first()

    if not record:
        db.close()
        return {"error": "Candidate not found"}

    if data.action == "shortlist":
        record.selected = True
    elif data.action == "reject":
        record.selected = False

    record.selection_reason = data.reason

    db.commit()
    db.close()

    return {"message": f"Candidate {data.action}ed successfully"}