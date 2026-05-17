import torch
import torch.nn as nn
import download_model

from transformers import (
    AutoTokenizer,
    AutoModel
)



# DEVICE

device = torch.device("cpu")



# TOKENIZER

tokenizer = AutoTokenizer.from_pretrained(
    "bert-base-uncased"
)

# SIMILARITY MODEL


class SimilarityModel(nn.Module):

    def __init__(self):

        super().__init__()

        # BERT MODEL
        self.bert = AutoModel.from_pretrained(
            "bert-base-uncased"
        )

        # FREEZE BERT
        for param in self.bert.parameters():

            param.requires_grad = False

        # CLASSIFIER HEAD
        self.fc = nn.Sequential(

            nn.Linear(768 * 3, 256),

            nn.ReLU(),

            nn.Dropout(0.3),

            nn.Linear(256, 1),

            nn.Sigmoid()
        )

    def forward(

        self,

        jd_inputs,

        resume_inputs
    ):

        # JD EMBEDDING
        jd_vec = self.bert(
            **jd_inputs
        ).pooler_output

        # RESUME EMBEDDING
        resume_vec = self.bert(
            **resume_inputs
        ).pooler_output

        # DIFFERENCE VECTOR
        diff = torch.abs(
            jd_vec - resume_vec
        )

        # CONCATENATE
        combined = torch.cat(

            [
                jd_vec,
                resume_vec,
                diff
            ],

            dim=1
        )

        # FINAL SCORE
        score = self.fc(combined)

        return score.squeeze()

# LOAD TRAINED MODEL

model = SimilarityModel()
model.load_state_dict(

    torch.load(
        "resume_model.pth",
        map_location=device
    )
)

model.to(device)

model.eval()

print("ATS MODEL LOADED")


# SEMANTIC SIMILARITY

def compute_similarity(

    job_description,

    resume_text
):

    # TOKENIZE JOB DESCRIPTION
    jd_inputs = tokenizer(

        job_description,

        return_tensors="pt",

        truncation=True,

        padding=True,

        max_length=128
    )

    # TOKENIZE RESUME
    resume_inputs = tokenizer(

        resume_text,

        return_tensors="pt",

        truncation=True,

        padding=True,

        max_length=128
    )

    # MOVE TO DEVICE
    jd_inputs = {

        k: v.to(device)

        for k, v in jd_inputs.items()
    }

    resume_inputs = {

        k: v.to(device)

        for k, v in resume_inputs.items()
    }

    # PREDICTION
    with torch.no_grad():

        similarity = model(

            jd_inputs,

            resume_inputs
        )

    return round(

        float(similarity.item()) * 100,

        2
    )



# SKILL MATCH FUNCTION

def skill_match(resume_skills, job_skills):
    if not job_skills:
        return 0, []

    matched = list(set(resume_skills) & set(job_skills))
    missing = list(set(job_skills) - set(resume_skills))

    score = (len(matched) / len(job_skills)) * 100

    return float(score), missing



# FINAL SCORE

def final_score(similarity, skill_score):
    return (0.5 * similarity) + (0.5 * skill_score)