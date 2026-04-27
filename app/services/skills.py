import re

# ✅ ADD THIS (IMPORTANT)
SKILLS_DB = {
    "data_science": ["python", "pandas", "numpy", "matplotlib", "seaborn", "machine learning"],
    "machine_learning": ["machine learning", "scikit-learn", "tensorflow", "keras"],
    "deep_learning": ["deep learning", "cnn", "rnn", "pytorch"]
}


def extract_skills(text):
    text = text.lower()

    found_skills = set()

    # flatten all skills
    all_skills = []
    for skills in SKILLS_DB.values():
        all_skills.extend(skills)

    # remove duplicates
    all_skills = list(set(all_skills))

    for skill in all_skills:
        ppattern = re.escape(skill.lower())
        if re.search(pattern, text):
            found_skills.add(skill.lower())

    return list(found_skills)