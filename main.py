from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/query", response_class=HTMLResponse)
async def get_started(request: Request):
    return templates.TemplateResponse("query.html", {"request": request})

@app.get("/itinerary", response_class=HTMLResponse)
async def plan_trip(request: Request, city: str):
    return templates.TemplateResponse("results.html", {"request": request, "city": city})

@app.post("/recommendations")
def get_recommendations(city: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_full_workflow, city)
    return {"message": f"Processing recommendations for {city} in background."}

def run_full_workflow(city: str):
    from DataCollector import getRedditData
    from GeminiProcessor import processData
    getRedditData(city)
    response = processData(city)
    print(response)

    
