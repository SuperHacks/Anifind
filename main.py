from flask import Flask
from flask import Blueprint
from dotenv import load_dotenv
from flask import request, redirect, url_for, session, render_template
print("This Worked")

views = Blueprint(__name__, "views")

@views.route("/")
def home():
    return print("This Worked")

@views.route("/my-Animes",methods=['POST', 'GET'])
def my_Animes():
    return print("url")