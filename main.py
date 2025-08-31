from flask import Blueprint
from flask import request, redirect, url_for, session, render_template
import secrets
from src.mal_api import MAL

api = MAL()
#params = ["title","synopsis","genres","related_anime"]
# Cowboy Bebop is ID: 1
#print(api.request(1,params))


views = Blueprint(__name__, "views")

token = secrets.token_urlsafe(100)
verifier = challenge = token[:128] 
state = "generaterandstring1"

@views.route("/")
def home():
    return redirect(api.authorize("http://localhost:8000/next", challenge, state), code=302)


@views.route("/next")
def next():
    code = request.args['code']
    session["access_token"] = api.getToken(code, verifier)
    print(session["access_token"])
    return code