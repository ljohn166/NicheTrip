from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from pydantic import BaseModel
import Recommendation

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents= "string input from user",
    config={
        "response_mime_type": "application/json",
        "response_schema": list[Recommendation],
    },
    config=types.GenerateContentConfig(
         system_instructions="keep it medium length and concise, assume user is smart, locations that are frequented by locals are preffered",
        thinking_config=types.ThinkingConfig(thinking_budget=-1),   
    ),
)

client.close() 