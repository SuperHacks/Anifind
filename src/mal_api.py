import json 
import requests 
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class MAL:
    def __init__(self):
        self.CLIENT_ID = os.getenv("MAL_CLIENT_ID")
        self.URL = "https://api.myanimelist.net/v2/anime/"
    
    def request(self, anime_id, params):
        """
        anime_id - Number corresponding to anime ID (Integer)
        params - List of parameters for desired request (List)
        """
        # No OAuth2
        link = self.URL + str(anime_id) + "?fields=" + ",".join(params)
        response = requests.get(link, headers = {'X-MAL-CLIENT-ID': self.CLIENT_ID})

        if response.status_code == 200:
            data = response.json()
        else:
            print(f"Error: {response.status_code}")
            print(response)
            data = None
        return data