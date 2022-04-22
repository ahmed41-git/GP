from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
import json
import urllib.request
import requests

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tmp/myDb.db"
db = SQLAlchemy(app)
migrate = Migrate(app,db)

from api import routes