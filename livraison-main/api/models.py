from datetime import datetime
from flask import Flask
from flask_login import login_user, UserMixin, LoginManager
from api import db

models = Flask(__name__)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    discriminator = db.Column('type', db.String(50))
    numero_telephone = db.Column(db.String(9), unique=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    __mapper_args__ = {'polymorphic_on': discriminator}


class Paiement(db.Model):
    numTransaction = db.Column(db.Integer, primary_key=True)
    #idColis = db.Column(db.Integer)
    #idVoyage = db.Column(db.Integer)
    idLivraison = db.Column(db.Integer)
    date = db.Column(db.String(60))
    statut = db.Column(db.Integer)

    def __repr__(self):
        return '<Paiement {}>'.format(self.numTransaction)

class Livraison(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idColis = db.Column(db.Integer)
    idVoyage = db.Column(db.Integer)
    idDestinataire = db.Column(db.Integer)
    date = db.Column(db.String(60))
    paiement = db.Column(db.Integer)
    livraison = db.Column(db.Integer)

    def __repr__(self):
        return '<Livraison {}>'.format(self.id)





class Admin(User):
    __mapper_args__ = {'polymorphic_identity': 'admin'}
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    nom = db.Column(db.String(50), nullable=True)
    prenom = db.Column(db.String(50), nullable=True)


class Client(User):
    __mapper_args__ = {'polymorphic_identity': 'client'}
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    nom = db.Column(db.String(50), nullable=True)
    prenom = db.Column(db.String(50), nullable=True)


class Livreur(User):
    __mapper_args__ = {'polymorphic_identity': 'livreur'}
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    img = db.Column(db.String(100))

