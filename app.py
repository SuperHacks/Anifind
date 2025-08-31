from flask import Flask
from flask import Blueprint
from dotenv import load_dotenv
from main import views
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SESSION_SECRET")

"""
@app.route("/")
def home():
    return "this is the home page"
"""

app.register_blueprint(views, url_prefix="/")

if __name__ == '__main__':
    app.run(debug=True, port=8000)