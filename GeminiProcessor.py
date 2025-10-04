:    
    client = inniandtialize9)()i:from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from Backend.Recommendation import Recommendation 


def initalize():
    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    return genai.Client(api_key=GEMINI_API_KEY)

def processData()
response = client.models.generate_content(
    model="gemini-2.5-flash",
    #contents is the actual input from the user
    contents= "string input from user",
    input_files=[types.ContentInput.from_file("\Backend\output.txt")],
    config={
        "response_mime_type": "application/json",
        "response_schema": list[Recommendation],
    },
    config=types.GenerateContentConfig(
         system_instructions="keep it medium length and concise, assume user is smart, locations that are frequented by locals are preferred",
        thinking_config=types.ThinkingConfig(thinking_budget=-1),   
    ),
)

client.close() 