from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from Recommendation import Recommendation 

def processData(location):
    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=GEMINI_API_KEY)


    prompt = (
    "You are a travel recommendation assistant helping a user plan a trip to " + location + 
    ". The user is looking for local, niche, or hidden gem locations in their destination — "
    "places that locals enjoy but aren’t crowded or overly touristy. These could include "
    "restaurants, cafes, parks, museums, cultural experiences, outdoor activities, local events, "
    "unique shops, or any interesting spots and experiences that capture the essence of the city. "
    "The user frequents Reddit and prefers recommendations sourced from Reddit users; however, "
    "only consider posts directly relevant to the city and its unique features. Do not directly quote "
    "redditors; instead, describe the locations and experiences in your own words, highlighting what makes "
    "them special and worth visiting."
    )


    reddit_file = client.files.upload(file="output.txt")


    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents = [reddit_file, prompt],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema= list[Recommendation],
            thinking_config=types.ThinkingConfig(thinking_budget=-1)
        ),
    )

    client.close()
    return response.text 

print(processData("Chicago"))