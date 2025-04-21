from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from diagnose_llm import get_llm_diagnosis
import uvicorn

app = FastAPI()

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load templates directory
templates = Jinja2Templates(directory="templates")

class DiagnoseInput(BaseModel):
    issue: str

@app.get("/", response_class=HTMLResponse)
async def serve_ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/diagnose")
async def diagnose_endpoint(input: DiagnoseInput):
    try:
        response = get_llm_diagnosis(input.issue)
        return {
            "translated": input.issue,
            "diagnosis": response,
            "estimated_cost": "3500"  # Placeholder or link to pricing model
        }
    except Exception as e:
        return {"error": str(e)}

# Only needed for local run
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
