import re
import spacy
from PyPDF2 import PdfReader

# Load NLP model once (fast)
nlp = spacy.load("en_core_web_sm")


# -----------------------------
# Extract text from PDF
# -----------------------------
def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content + "\n"

    return text


# -----------------------------
# Extract Email
# -----------------------------
def extract_email(text):
    match = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return match[0] if match else "Not Found"


# -----------------------------
# Extract Phone
# -----------------------------
def extract_phone(text):
    match = re.findall(r"\+?\d[\d\s-]{8,}\d", text)
    return match[0] if match else "Not Found"


# -----------------------------
# Extract Name (BEST METHOD)
# -----------------------------
def extract_name(text):
    doc = nlp(text[:1000])  # limit for speed

    # Try NER first
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text.strip()

            if len(name.split()) >= 2:
                return name

    # Fallback method
    lines = text.split("\n")

    for line in lines[:10]:
        line = line.strip()

        if not line:
            continue

        if line.upper() in ["CONTACT", "RESUME", "CV", "PROFILE"]:
            continue

        if "@" in line or any(char.isdigit() for char in line):
            continue

        if len(line.split()) <= 4:
            return line

    return "Unknown"


# -----------------------------
# MAIN FUNCTION
# -----------------------------
def parse_resume(file_path):
    text = extract_text_from_pdf(file_path)

    return {
        "text": text,
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text)
    }