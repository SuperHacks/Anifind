from mal_api import MAL
from sqlite_loader import SQLITE
import time
import json

mal = MAL()
db = SQLITE("anime.db", new=True)
FILEDS = ["title", "genres", "synopsis", "related_anime"]

for anime_id in range(1, 60001):
    try:
        data = mal.request(anime_id, FILEDS)
        if data:  
            genres = ",".join([g["name"] for g in data.get("genres", [])])
            related_ids = [r["node"]["id"] for r in data.get("related_anime", [])]

            anime_row = {
                "id": data["id"],
                "title": data.get("title"),
                "synopsis": data.get("synopsis", ""),
                "genres": genres,
                "related": related_ids
            }

            db.insert(anime_row)
            print(f"Inserted anime {anime_id}: {data.get('title')}")

    except Exception as e:
        print(f"Error on anime {anime_id}: {e}")
    

    print("Finished fetching and storing anime.")
db.close()