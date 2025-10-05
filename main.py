from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from DataCollector import getRedditData
from GeminiProcessor import processData

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/recommendations")
def get_recommendations(city: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_full_workflow, city)
    return {"message": f"Processing recommendations for {city} in background."}

def run_full_workflow(city: str):
    getRedditData(city)
    response = processData(city)
    print(response)

    
