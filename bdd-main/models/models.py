from datetime import datetime
from flask import Flask
#from flask_login import login_user, UserMixin, LoginManager
from __main__ import db

models = Flask(__name__)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	numero_telephone = db.Column(db.String(9), unique=True)
	

class Admin(User):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100), unique=True, nullable=False)

class Client(User):
	id = db.Column(db.Integer, primary_key=True)
	

class Livreur(User):
	id = db.Column(db.Integer, primary_key=True)
	nom = db.Column(db.String(50), nullable=False)
	prenom = db.Column(db.String(50), nullable=False)
	img = db.Column(db.String(100))
							
		
			

class Livraison(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	#adresse_depart = db.Column(db.String(100))
	numero_destinataire = db.Column(db.String(9));#optionnel
	date = db.Column(db.Datetime, nullable=False, default=datetime.utcnow);
	#heure = ;	