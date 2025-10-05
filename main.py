from fastapi import FastAPI, Request, Form, BackgroundTasks, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json
from database import init_db, get_from_db, save_to_db
from validate import is_valid_city
from fastapi.responses import JSONResponse
import os

app = FastAPI()

init_db()


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/query", response_class=HTMLResponse)
async def get_started(request: Request):
    return templates.TemplateResponse("query.html", {"request": request})

# @app.get("/itinerary", response_class=HTMLResponse)
# async def plan_trip(request: Request, city: str = Query(...)):
    
        

    #     return templates.TemplateResponse("itinerary.html", {
    #     "request": request,
    #     "city": city,
    #     "places": places
    # })

@app.post("/itinerary")
def get_recommendations(request: Request, city: str = Form(...)):
    if not is_valid_city(city):
        return templates.TemplateResponse("query.html", {
            "request": request,
            "error": f"'{city}' is not a recognized city. Please enter a valid city name."
        })
    
    cached_response = get_from_db(city)
    if cached_response:
        return templates.TemplateResponse("itinerary.html", {
            "request": request,
            "city": city,
            "places": cached_response
        })

    from DataCollector import getRedditData
    from GeminiProcessor import processData
    
    getRedditData(city)
    response = processData(city)
    response = json.loads(response)
    save_to_db(city, response)
    print(response)
    return templates.TemplateResponse("itinerary.html", {
        "request": request,
        "city": city,
        "places": response
    })
    
