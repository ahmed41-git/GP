from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://ahmed:passer123@localhost/flask_db"
db=SQLAlchemy(app)


from api import routes, modules