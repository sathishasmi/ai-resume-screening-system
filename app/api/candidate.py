from fastapi import APIRouter, UploadFile, File, Form
import tempfile
import os

from app.services.parser import parse_resume
from app.services.skills import extract_skills, SKILLS_DB
from app.services.matcher import compute_similarity, final_score, skill_match

from app.core.database import SessionLocal
from app.models.candidate import Candidate
from app.models.analysis import Analysis
from app.models.job import Job

router = APIRouter()


@router.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    job_id: int = Form(...)
):
    db = SessionLocal()

    try:
        # =========================
        # Save uploaded file
        # =========================
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
            temp.write(await file.read())
            temp_path = temp.name

        # =========================
        # Parse Resume
        # =========================
        parsed = parse_resume(temp_path)

        text = parsed.get("text", "")
        name = parsed.get("name", "Unknown")
        email = parsed.get("email", "Not Found")
        phone = parsed.get("phone", "Not Found")

        # =========================
        # Get Job from DB
        # =========================
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return {"error": "Job not found"}

        job_desc = str(job.description)
        job_title = str(job.title)

        # =========================
        # Extract Resume Skills
        # =========================
        resume_skills = extract_skills(text)

        # =========================
        # 🔥 TOP 3 DOMAIN MATCH LOGIC
        # =========================
        domain_scores = {}

        for domain, skills in SKILLS_DB.items():

            # normalize
            resume_set = set([s.lower().strip() for s in resume_skills])
            job_set = set([s.lower().strip() for s in skills])

            match_count = 0

            for job_skill in job_set:
                for resume_skill in resume_set:
                    if job_skill in resume_skill or resume_skill in job_skill:
                        match_count += 1
                        break

            score = (match_count / len(job_set)) * 100 if job_set else 0
            domain_scores[domain] = round(score, 2)

        # Sort and get top 3
        sorted_domains = sorted(domain_scores.items(), key=lambda x: x[1], reverse=True)
        top_domains = sorted_domains[:3]

        # =========================
        # Matching with selected job
        # =========================
        job_skills = extract_skills(job_desc)

        similarity = compute_similarity(text, job_desc)
        skill_score, missing = skill_match(resume_skills, job_skills)

        score = final_score(similarity, skill_score)

        # =========================
        # Save Candidate
        # =========================
        candidate = Candidate(
            name=name,
            email=email,
            phone=phone,
            resume_file=temp_path,
            job_id=job_id
        )

        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        # =========================
        # Save Analysis
        # =========================
        analysis = Analysis(
            candidate_id=candidate.id,
            domain=job_title,
            score=round(score, 2),
            missing_skills=", ".join(missing),
            selected=0,
            selection_reason=""
        )

        db.add(analysis)
        db.commit()

        # =========================
        # Response (IMPORTANT)
        # =========================
        return {
            "name": name,
            "job": job_title,
            "score": round(score, 2),
            "similarity": round(similarity, 2),
            "skill_score": round(skill_score, 2),
            "missing_skills": missing,

            # 🔥 NEW (for chart)
            "top_domains": [
                {"domain": d[0], "score": d[1]} for d in top_domains
            ]
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        db.close()