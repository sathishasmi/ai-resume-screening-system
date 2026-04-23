import re

SKILLS_DB = {

    # -----------------------------
    # DATA SCIENCE / ML
    # -----------------------------
    "data_science": [
        "python", "pandas", "numpy", "matplotlib", "seaborn",
        "machine learning", "ml", "scikit-learn",
        "data analysis", "statistics"
    ],

    "machine_learning": [
        "machine learning", "ml", "scikit-learn",
        "model building", "feature engineering"
    ],

    "deep_learning": [
        "deep learning", "tensorflow", "keras", "pytorch"
    ],

    "data_analyst": [
        "excel", "sql", "power bi", "tableau",
        "data visualization"
    ],

    # -----------------------------
    # BACKEND DEVELOPMENT
    # -----------------------------
    "backend_developer": [
        "python", "java", "node.js",
        "fastapi", "django", "flask",
        "rest api", "api development"
    ],

    # -----------------------------
    # FRONTEND DEVELOPMENT
    # -----------------------------
    "frontend_developer": [
        "html", "css", "javascript",
        "react", "angular", "vue"
    ],

    # -----------------------------
    # FULL STACK
    # -----------------------------
    "full_stack": [
        "javascript", "react", "node.js",
        "mongodb", "sql", "api"
    ],

    # -----------------------------
    # DEVOPS / CLOUD
    # -----------------------------
    "devops": [
        "docker", "kubernetes", "ci/cd",
        "aws", "azure", "linux"
    ],

    "cloud_engineer": [
        "aws", "azure", "gcp",
        "cloud computing"
    ],

    # -----------------------------
    # DATABASE
    # -----------------------------
    "database": [
        "sql", "mysql", "postgresql",
        "mongodb"
    ]
}


def extract_skills(text):
    text = text.lower()
    found = set()

    for skill, variants in SKILLS_DB.items():
        for v in variants:
            pattern = r"\b" + re.escape(v) + r"\b"
            if re.search(pattern, text):
                found.add(skill)
                break

    return list(found)