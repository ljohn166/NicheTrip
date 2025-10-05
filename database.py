import sqlite3
import json

DB_PATH = "recommendations.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS city_recommendations (
            city TEXT PRIMARY KEY,
            response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def get_from_db(city: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT response FROM city_recommendations WHERE city = ?", (city,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return None

def save_to_db(city: str, response: dict):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO city_recommendations (city, response) VALUES (?, ?)",
        (city, json.dumps(response))
    )
    conn.commit()
    conn.close()

def delete_city(city: str):
    """
    Deletes the cached recommendation for a given city from the database.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM city_recommendations WHERE city = ?", (city,))
    conn.commit()
    conn.close()


city_to_delete = input("Enter the city to delete: ")
delete_city(city_to_delete)
print(f"Deleted cached data for {city_to_delete}")