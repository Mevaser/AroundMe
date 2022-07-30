from flask import Flask
from flask_googlemaps import GoogleMaps
from flask_mobility import Mobility
from config import Config
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
Mobility(app)
GoogleMaps(app, key=Config.GOOGLE_KEY)

app.config.from_object(Config)
from app import routes
