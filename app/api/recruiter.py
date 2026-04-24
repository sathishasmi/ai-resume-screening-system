from fastapi import APIRouter
from pydantic import BaseModel

from app.core.database import SessionLocal
from app.models.candidate import Candidate
from app.models.analysis import Analysis
from app.models.job import Job

router = APIRouter()


# -----------------------------
# Create Job
# -----------------------------
@router.post("/recruiter/create-job")
def create_job(title: str, description: str):
    db = SessionLocal()

    job = Job(title=title, description=description)
    db.add(job)
    db.commit()
    db.refresh(job)

    db.close()
    return {"message": "Job created", "job_id": job.id}


# -----------------------------
# Get Jobs (for dropdown)
# -----------------------------
@router.get("/jobs")
def get_jobs():
    db = SessionLocal()
    jobs = db.query(Job).all()
    db.close()
    return jobs


# -----------------------------
# Get Candidates (Dashboard)
# -----------------------------
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
            "reason": a.selection_reason
        }
        for c, a in data
    ]


# -----------------------------
# Shortlist / Reject
# -----------------------------
class DecisionRequest(BaseModel):
    id: int
    action: str
    reason: str


@router.post("/recruiter/decision")
def decide_candidate(data: DecisionRequest):
    db = SessionLocal()

    record = db.query(Analysis).filter(Analysis.id == data.id).first()

    if not record:
        db.close()
        return {"error": "Candidate not found"}

    if data.action == "shortlist":
        record.selected = 1
    elif data.action == "reject":
        record.selected = 0

    record.selection_reason = data.reason

    db.commit()
    db.close()

    return {"message": "Updated"}