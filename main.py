from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return{"layout.html"}

"""@app.post("/itinerary")
def get_item(item_id: String):
    if get:

    else:
        return render_template("index.html")"""