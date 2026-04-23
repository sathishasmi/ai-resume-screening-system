from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

# Routers
from app.api.candidate import router as candidate_router
from app.api.recruiter import router as recruiter_router

app = FastAPI()

# Templates
templates = Jinja2Templates(directory="app/templates")

# Static files (optional but recommended)
#app.mount("/static", StaticFiles(directory="app/static"), name="static")


# -----------------------------
# Home Page (Candidate UI)
# -----------------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",   # ✅ correct position
        {"request": request}
    )

@app.get("/recruiter", response_class=HTMLResponse)
async def recruiter_page(request: Request):
    return templates.TemplateResponse(
        request,
        "recruiter.html",
        {"request": request}
    )

# -----------------------------
# Include Routers
# -----------------------------
app.include_router(candidate_router)
app.include_router(recruiter_router)

from app.core.database import Base, engine
from app.models import candidate, analysis

Base.metadata.create_all(bind=engine)