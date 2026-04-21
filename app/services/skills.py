SKILLS_DB = {
    "python": ["python"],
    "sql": ["sql"],
    "machine learning": ["ml", "machine learning"],
    "javascript": ["js", "javascript"],
    "react": ["react"],
    "aws": ["aws", "amazon web services"],
    "docker": ["docker"],
    "excel": ["excel"]
}

def extract_skills(text):
    found = []
    for skill, variants in SKILLS_DB.items():
        if any(v in text for v in variants):
            found.append(skill)
    return found