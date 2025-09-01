import json 
import requests 
import os
import urllib.parse
from pathlib import Path
import time
from dotenv import load_dotenv

load_dotenv()
max_retries = 3
class MAL:
    def __init__(self):
        self.CLIENT_ID = os.getenv("MAL_CLIENT_ID")
        self.CLIENT_SECRET = os.getenv("MAL_CLIENT_SECRET")
        self.URL = "https://api.myanimelist.net/v2/anime/"
        self.AUTH = "https://myanimelist.net/v1/oauth2/authorize?"
    
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
            print(f"Error: {response.status_code}")
            print(response)
            data = None
        return data
    
    def authorize(self, redirectURL, challenge, state):

        params={
            "response_type": "code",
            "client_id": self.CLIENT_ID,
            "code_challenge": challenge,
            "state": state,
            "redirect_uri": redirectURL
        }
        url = self.AUTH + urllib.parse.urlencode(params)

        return url
    
    def getToken(self, code, verifier, redirectURL):

        head = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        body = {
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET,
            "code" : code,
            "code_verifier": verifier,
            "grant_type" : "authorization_code",
            "redirect_uri": redirectURL
        }
        #Need to change flow so that new token is only grabbed for first time users otherwise use refresh token to refresh
        req = requests.post("https://myanimelist.net/v1/oauth2/token", data=body, headers=head)
        resp = json.loads(req.text)
        return resp["access_token"]
    
    def getUserList(self, at):
        auth_header = {
            "Authorization": "Bearer {}".format(at) 
        }
        params = {
            "status": "completed",
            "limit": 1000
        }
        endpoint = "https://api.myanimelist.net/v2/users/@me/animelist?"
        resp = requests.get(endpoint, headers=auth_header, params=params)
        animeList = json.loads(resp.text)
        return animeList

