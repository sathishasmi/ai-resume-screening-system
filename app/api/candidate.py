from fastapi import APIRouter, UploadFile, File, Form
import tempfile
import os
import numpy as np

from app.services.parser import parse_resume
from app.services.skills import extract_skills
from app.services.matcher import compute_similarity, final_score, skill_match
from app.models.loader import load_domain_model

from app.core.database import SessionLocal
from app.models.candidate import Candidate
from app.models.analysis import Analysis

router = APIRouter()

# Load ML model once
model = load_domain_model()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    job_desc: str = Form(...)
):
    try:
        # -----------------------------
        # 1. Save file temporarily
        # -----------------------------
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
            temp.write(await file.read())
            temp_path = temp.name

        # -----------------------------
        # 2. Parse resume (IMPORTANT)
        # -----------------------------
        parsed = parse_resume(temp_path)

        text = parsed["text"]
        name = parsed["name"]
        email = parsed["email"]
        phone = parsed["phone"]

        # -----------------------------
        # 3. Extract skills
        # -----------------------------
        resume_skills = extract_skills(text)
        job_skills = extract_skills(job_desc)

        # -----------------------------
        # 4. Domain Prediction
        # -----------------------------
        predicted_domain = model.predict([text])[0]
        probs = model.predict_proba([text])[0]

        confidence = f"{round(float(max(probs) * 100), 2)}%"

        top_indices = np.argsort(probs)[-3:][::-1]

        top_domains = [
            {
                "domain": model.classes_[i],
                "score": round(float(probs[i] * 100), 2)
            }
            for i in top_indices
        ]

        # -----------------------------
        # 5. Similarity + Skill match
        # -----------------------------
        similarity = compute_similarity(text, job_desc)

        skill_score, missing = skill_match(resume_skills, job_skills)

        matched = list(set(resume_skills) & set(job_skills))

        reason = (
            f"Matched skills: {', '.join(matched)}"
            if matched else "No strong skill match found"
        )

        # -----------------------------
        # 6. Final Score
        # -----------------------------
        score = final_score(similarity, skill_score)

        # -----------------------------
        # 7. Save to DB
        # -----------------------------
        db = SessionLocal()

        candidate = Candidate(
            name=name,
            email=email,
            phone=phone,
            resume_file=temp_path
        )
        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        analysis = Analysis(
            candidate_id=candidate.id,
            domain=predicted_domain,
            score=round(score, 2),
            missing_skills=",".join(missing)
        )
        db.add(analysis)
        db.commit()
        db.close()

        # -----------------------------
        # 8. Response
        # -----------------------------
        return {
        "name": name,
        "email": email,
        "phone": phone,
        "predicted_domain": predicted_domain,
        "confidence": round(float(max(probs) * 100), 2),
        "top_predictions": top_domains,
        "match_score": round(score, 2),
        "similarity_score": round(similarity, 2),
        "skill_score": round(skill_score, 2),
        "missing_skills": missing or [],
        "reason": reason
    }

    except Exception as e:
        return {"error": str(e)}