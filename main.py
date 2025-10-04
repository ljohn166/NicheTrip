from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return{"index.html"}

@app.post("/results")
def get_item(item_id: String)