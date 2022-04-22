from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
import json
import urllib.request
import requests

app.config["SECRET_KEY"] = "br@d@fr@m@n@d@m@d@"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tmp/myDb.db"
db = SQLAlchemy(app)
ma = Marshmallow(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

from api import routes