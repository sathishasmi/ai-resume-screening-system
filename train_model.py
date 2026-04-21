import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv("datasets/resume_dataset_1200.csv")

# -----------------------------
# Create better text
# -----------------------------
df["resume_text"] = (
    df["Skills"].fillna("") + " " +
    df["Field_of_Study"].fillna("") + " " +
    df["Current_Job_Title"].fillna("")
).str.lower()

# -----------------------------
# Clean domain labels (VERY IMPORTANT)
# -----------------------------
def clean_domain(title):
    title = str(title).lower()

    if any(x in title for x in ["data", "ml", "machine learning", "ai", "analytics"]):
        return "Data Science"
    elif any(x in title for x in ["frontend", "react", "angular"]):
        return "Frontend"
    elif any(x in title for x in ["backend", "django", "flask", "node"]):
        return "Backend"
    elif any(x in title for x in ["developer", "engineer"]):
        return "Software Engineer"
    else:
        return "Other"

df["domain"] = df["Current_Job_Title"].apply(clean_domain)

# -----------------------------
# REMOVE weak class
# -----------------------------
df = df[df["domain"] != "Other"]

# -----------------------------
# Train
# -----------------------------
X = df["resume_text"]
y = df["domain"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words="english", ngram_range=(1,2))),
    ("clf", LogisticRegression(max_iter=1000))
])

model.fit(X_train, y_train)

print("Accuracy:", model.score(X_test, y_test))

joblib.dump(model, "domain_model.pkl")
print("Model saved!")