import json 
import requests 
import os
from pathlib import Path
import time
from dotenv import load_dotenv

load_dotenv()
max_retries = 3
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
        
        for attempt in range(max_retries):
            try:
                response = requests.get(link, headers = {'X-MAL-CLIENT-ID': self.CLIENT_ID},timeout=10)
                response.raise_for_status()
                print("Success!")
                break  # exit loop if successful
            except requests.exceptions.Timeout:
                print(f"Timeout, retrying ({attempt+1}/{max_retries})...")
                time.sleep(60)  # wait 
            except requests.exceptions.RequestException as e:
                #print(f"Other error: {e}")
                break
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return None