# app/api/routes.py

from fastapi import APIRouter, UploadFile, File, Form
import tempfile
import os
import numpy as np

from app.services.parser import extract_text
from app.services.skills import extract_skills
from app.services.matcher import compute_similarity, final_score, skill_match
from app.models.loader import load_domain_model

# -----------------------------------
# Initialize
# -----------------------------------

router = APIRouter()

# Load ML model once (IMPORTANT)
model = load_domain_model()

# Ensure uploads folder exists
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -----------------------------------
# TEST ROUTE (DEBUG)
# -----------------------------------

@router.get("/test-model")
def test_model():
    import numpy as np

    text = "python machine learning data analysis"

    prediction_domain = model.predict([text])[0]
    probs = model.predict_proba([text])[0]

    # Confidence (string with %)
    confidence = f"{round(float(max(probs) * 100), 2)}%"

    # Top 3 predictions
    top_indices = np.argsort(probs)[-3:][::-1]

    top_domains = [
        {
            "domain": model.classes_[i],
            "score": round(float(probs[i] * 100), 2)
        }
        for i in top_indices
    ]

    return {
        "input": text,
        "predicted_domain": prediction_domain,
        "confidence": confidence,
        "top_predictions": top_domains
    }

# -----------------------------------
# MAIN ANALYZE ROUTE
# -----------------------------------

@router.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    job_desc: str = Form(...)
):
    try:
        # 1. Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
            temp.write(await file.read())
            temp_path = temp.name

        print("File saved at:", temp_path)

        # 2. Extract text from resume
        text = extract_text(temp_path)

        if not text or len(text.strip()) == 0:
            return {"error": "Failed to extract text from resume"}

        print("Extracted text:", text[:200])

        # 3. Extract skills
        resume_skills = extract_skills(text)
        job_skills = extract_skills(job_desc)

        print("Resume Skills:", resume_skills)
        print("Job Skills:", job_skills)

        # 4. Domain prediction
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

        # 5. Similarity score
        similarity = compute_similarity(text, job_desc)

        # 6. Skill match score
        skill_score, missing = skill_match(resume_skills, job_skills)

        matched = list(set(resume_skills) & set(job_skills))

        reason = (
            f"Matched skills: {', '.join(matched)}"
            if matched else
            "No strong skill match found"
        )

        # 7. Final score
        score = final_score(similarity, skill_score)

        # 8. Response
        return {
            "predicted_domain": predicted_domain,
            "confidence": confidence,
            "top_predictions": top_domains,
            "match_score": round(score, 2),
            "similarity_score": round(similarity, 2),
            "skill_score": round(skill_score, 2),
            "missing_skills": missing,
            "reason": reason 
        }

    except Exception as e:
        return {"error": str(e)}