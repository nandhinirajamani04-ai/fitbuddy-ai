from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from .database import (
    save_user_plan,
    get_all_users,
    save_feedback
)

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
       name="index.html",
       context=
        {
            "request": request
        }
    )


@router.post("/save-user-plan")
async def save_user_plan_route(
    user_id: str = Form(""),
    name: str = Form(""),
    age: str = Form(""),
    weight: str = Form(""),
    goal: str = Form(""),
    intensity: str = Form(""),
    original_plan: str = Form("")
):
    try:

        print("========== SAVE USER ==========")
        print("USER ID:", user_id)
        print("NAME:", name)
        print("AGE:", age)
        print("WEIGHT:", weight)
        print("GOAL:", goal)
        print("INTENSITY:", intensity)

        save_user_plan(
            user_id,
            name,
            int(age) if age else 0,
            float(weight) if weight else 0,
            goal,
            intensity,
            original_plan
        )

        return JSONResponse({
            "success": True,
            "message": "User plan saved successfully"
        })

    except Exception as e:

        print("SAVE ERROR:", e)

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": str(e)
            }
        )


@router.post("/submit-feedback")
async def submit_feedback(
    user_id: str = Form(...),
    feedback: str = Form(...)
):
    try:

        print("USER ID:", user_id)
        print("FEEDBACK:", feedback)

        save_feedback(user_id, feedback)

        return JSONResponse({
            "success": True,
            "message": "Feedback submitted and workout plan updated successfully!"
        })

    except Exception as e:

        print("FEEDBACK ERROR:", e)

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": str(e)
            }
        )

@router.get("/view-all-users", response_class=HTMLResponse)
async def view_all_users(request: Request):

    users = get_all_users()

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "request": request,
            "users": users
        }
    )
