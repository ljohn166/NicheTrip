import requests

def is_valid_city(city) -> bool:
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": city,
            "format": "json",
            "addressdetails": 1,
            "limit": 1
        }
        headers = {"User-Agent": "NicheTripApp/1.0 (whssave@gmail.com)"}
        response = requests.get(url, params=params, headers=headers, timeout=5)
        data = response.json()

        if not data:
            return False  # No results found

        place_type = data[0].get("type", "")
        valid_types = {"city", "town", "village", "municipality", "hamlet", "region", "administrative", "county"}

        return place_type in valid_types

    except Exception as e:
        print(f"Nominatim error, try again: {e}")
        return None