from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from pydantic import BaseModel


load_dotenv()

class Recommendation(BaseModel):
    Name: str
    Location: str
    description: str

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

#Initialize the client
client = genai.Client(api_key=GEMINI_API_KEY)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Generate places to see in Prague that are off the beaten path and aren't typically touristy. I am an adventerous traveler who likes to expereince a wide range of things in my destination. ",
    config={
        "response_mime_type": "application/json",
        "response_schema": list[Recommendation],
    },
    # config=types.GenerateContentConfig(
    #     #system_instructions="keep it medium length and concise, assume user is smart, ",
    #     thinking_config=types.ThinkingConfig(thinking_budget=-1),   
    # ),
)

print(response.text)


client.close() 
