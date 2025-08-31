from flask import Flask
from flask import Blueprint
from flask import request, redirect, url_for, session, render_template
from src.mal_api import MAL

api = MAL()
params = ["title","synopsis","genres","related_anime"]
# Cowboy Bebop is ID: 1
print(api.request(1,params))


views = Blueprint(__name__, "views")

@views.route("/")
def home():
    return print("This Worked")

@views.route("/my-Animes",methods=['POST', 'GET'])
def my_Animes():
    return print("url")