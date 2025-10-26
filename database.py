from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def init_db():
    pass

def get_from_db(city: str):
    try:
        city_response = supabase.table("city_recommendations").select("id").eq("city", city).single().execute()
        if not city_response.data:
            return None
        
        city_id = city_response.data["id"]
        recommendations_response = supabase.table("recommendations").select("*").eq("city_id", city_id).execute()
        
        if recommendations_response.data:
            return [_format_recommendation(rec) for rec in recommendations_response.data]
        return None
    except Exception as e:
        print(f"Error fetching from database: {e}")
        return None

def save_to_db(city: str, recommendations: list):
    try:
        city_response = supabase.table("city_recommendations").upsert({"city": city}).execute()
        city_id = city_response.data[0]["id"]
        
        supabase.table("recommendations").delete().eq("city_id", city_id).execute()
        
        for rec in recommendations:
            data = {
                "city_id": city_id,
                "name": rec.get("name"),
                "location_city": rec.get("location", {}).get("city"),
                "location_country": rec.get("location", {}).get("country"),
                "type": rec.get("type"),
                "description": rec.get("description"),
                "coordinates": rec.get("coordinates")
            }
            supabase.table("recommendations").insert(data).execute()
    except Exception as e:
        print(f"Error saving to database: {e}")

def delete_city(city: str):
    try:
        city_response = supabase.table("city_recommendations").select("id").eq("city", city).single().execute()
        if city_response.data:
            city_id = city_response.data["id"]
            supabase.table("recommendations").delete().eq("city_id", city_id).execute()
            supabase.table("city_recommendations").delete().eq("id", city_id).execute()
    except Exception as e:
        print(f"Error deleting from database: {e}")

def _format_recommendation(rec: dict) -> dict:
    return {
        "name": rec["name"],
        "location": {
            "city": rec["location_city"],
            "country": rec["location_country"]
        },
        "type": rec["type"],
        "description": rec["description"],
        "coordinates": rec.get("coordinates")
    }