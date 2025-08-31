import sqlite3
import json
import random

class SQLITE():
    def __init__(self,name,new):
        self.conn = sqlite3.connect(name)
        self.c = self.conn.cursor()
        if new:
            # Create table
            self.c.execute("""
            CREATE TABLE IF NOT EXISTS anime (
                id INTEGER PRIMARY KEY,
                title TEXT,
                synopsis TEXT,
                genres TEXT,
                related TEXT  -- JSON string of related IDs
            )""")
            self.conn.commit()

    def insert(self, anime_data):
        """
        anime_data: dict with keys 'id', 'title', 'synopsis', 'genres', 'related'
        'related' should be a list of IDs
        """
        self.c.execute("""
            INSERT OR REPLACE INTO anime (id, title, synopsis, genres, related)
            VALUES (?, ?, ?, ?, ?)
        """, (
            anime_data["id"],
            anime_data["title"],
            anime_data["synopsis"],
            anime_data["genres"],
            json.dumps(anime_data.get("related", []))
        ))
        self.conn.commit()

    def search(self, anime_id):
        """
        Returns the anime row as a dict with 'related' converted to a list,
        including the new fields: themes and demographic.
        """
        self.c.execute("SELECT * FROM anime WHERE id = ?", (anime_id,))
        row = self.c.fetchone()
        if row:
            return {
                "id": row[0],
                "title": row[1],
                "synopsis": row[2],
                "genres": row[3],
                "related": json.loads(row[4])  # convert JSON string back to list
            }
        else:
            return None

    def find_unrelated(self, anime_id):
        """
        Finds a random anime that is NOT related to the given anime_id
        and does NOT share genres, themes, or demographic.
        
        Hybrid approach: iterate through all anime, collect valid candidates, then pick randomly.
        """
        base = self.search(anime_id)
        if not base:
            return None

        # Convert base genres/themes to sets for easy comparison
        base_genres = set(g.strip() for g in base["genres"].split(",")) if base["genres"] else set()

        # Fetch all other anime
        self.c.execute("SELECT * FROM anime WHERE id != ?", (anime_id,))
        candidates = []

        for row in self.c.fetchall():
            related_ids = json.loads(row[4])  # related field is JSON

            # Skip if this anime is related to the base
            if anime_id in related_ids:
                continue

            # Convert candidate genres/themes to sets
            genres = set(g.strip() for g in row[3].split(",")) if row[3] else set()

            # Check criteria: no overlap in genres/themes and different demographic
            if genres.isdisjoint(base_genres):
                candidates.append({
                    "id": row[0],
                    "title": row[1],
                    "synopsis": row[2],
                    "genres": row[3],
                    "related": related_ids
                })

        # Return a random candidate if any
        if candidates:
            return random.choice(candidates)
        else:
            return None
    def close(self):
        self.conn.close()