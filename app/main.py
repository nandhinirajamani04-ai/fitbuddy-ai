from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .database import init_db
from .routes import router


BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(
    directory=str(BASE_DIR.parent / "templates")
)

app = FastAPI(
    title="FitBuddy - AI Workout Generator",
    version="1.0.0"
)


@app.on_event("startup")
def startup():
    init_db()


app.include_router(router)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="plan.html",
        context=
        {"request": request,
         "plan":None       }
    )