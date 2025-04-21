import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from llm.diagnose_llm import get_llm_diagnosis

app = FastAPI()

# CORS (allow all for testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Input schema
class DiagnoseInput(BaseModel):
    issue: str


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/diagnose")
async def diagnose(input: DiagnoseInput):
    try:
        diagnosis = get_llm_diagnosis(input.issue)

        return {
            "translated": input.issue,
            "diagnosis": diagnosis,
            "estimated_cost": "Not Available",  # update if cost logic added
            "products": []  # update if product logic added
        }

    except Exception as e:
        return {"error": str(e)}


# Optional: for local testing
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
