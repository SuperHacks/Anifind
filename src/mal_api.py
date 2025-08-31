import json 
import requests 
import os
import secrets
import base64
import hashlib
import re
import urllib.parse
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class MAL:
    def __init__(self):
        self.CLIENT_ID = os.getenv("MAL_CLIENT_ID")
        self.URL = "https://api.myanimelist.net/v2/anime/"
        self.AUTH = "https://myanimelist.net/v1/oauth2/authorize?"
    
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
    
    def getToken(self, code, verifier):

        head = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        body = {
            "client_id": self.CLIENT_ID,
            "code" : code,
            "code_verifier": verifier,
            "grant_type" : "authorization_code",
        }
        req = requests.post("https://myanimelist.net/v1/oauth2/token", data=body, headers=head)
        resp = json.loads(req.text)
        return resp["access_token"]

    