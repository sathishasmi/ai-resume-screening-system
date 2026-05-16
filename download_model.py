import os
import gdown

MODEL_PATH = "resume_model.pth"

FILE_ID = "YOUR_FILE_ID"

URL = f"https://drive.google.com/file/d/1P0mqh3pJLy6-xEGGnzb_8xfoF5reYa3k/view?usp=sharing"

if not os.path.exists(MODEL_PATH):
    print("Downloading model...")
    gdown.download(URL, MODEL_PATH, quiet=False)
    print("Model downloaded!")
else:
    print("Model already exists.")