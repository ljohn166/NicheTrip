from pydantic import BaseModel

class Location(BaseModel):
    city: str
    country: str
    # consider adding and importing google maps so we can incorporate into our project

class Recommendation(BaseModel):
    name: str
    description: str
    location: Location
    type: str

