from dataclasses import dataclass
from datetime import date, datetime, timezone
from enum import unique
import enum
from os import TMP_MAX
from api import db
import api.models

from sqlalchemy.orm import defaultload
from api import db

@dataclass
class User(db.Model):
    nom:str
    prenom:str
    telephone:str
    email:str
    password:str
    type:enum

    id = db.Column(db.Integer(), primary_key=True)
    nom= db.Column(db.String(length=32), nullable=False, unique=False)
    prenom=db.Column(db.String(length=32), nullable=False, unique=False)
    telephone=db.Column(db.String(length=32), nullable=False, unique=True)
    email=db.Column(db.String(length=32), nullable=False, unique=True)
    password=db.Column(db.String(length=32), nullable=False, unique=False)
    type=db.Column(db.Enum("gp", "client"), nullable=False, unique=False)
    __mapper_args__ = {'polymorphic_on': type}


    def __repr__(self) -> str:
        return self.nom+" "+self.prenom

@dataclass
class GP(User):
    categorie:enum
    __mapper_args__ = {'polymorphic_identity': 'gp'}
    id = db.Column(db.Integer(),db.ForeignKey('user.id'), primary_key=True)
    voyages = db.relationship("Voyage", backref="voyageur", lazy=True)
    categorie=db.Column(db.Enum("entreprise", "particulier"), nullable=False, unique=False)

@dataclass
class Client(User):
    __mapper_args__ = {'polymorphic_identity': 'client'}
    id = db.Column(db.Integer(),db.ForeignKey('user.id'), primary_key=True)


@dataclass
class Colis(db.Model):
    type_colis : enum
    poids:float
    forme:enum
    id = db.Column(db.Integer(), primary_key=True)
    type_colis=db.Column(db.Enum(".....", "type11"), nullable=False, unique=False)
    poids=db.Column(db.Float(), nullable=False, unique=False)
    forme=db.Column(db.Enum("forme1", "..."), nullable=False, unique=False)
    voyage_id=db.Column(db.Integer(),db.ForeignKey('voyage.id'), nullable=True)
    def add_colis(self,id):
        self.gp_id=db.session.query(GP).filter_by(id=id).first().id
@dataclass
class Voyage(db.Model):
    date_depart:datetime
    date_arrive:datetime
    adresse_depart:str
    adresse_arrive:str
    nombre_kg_disponible:int
    tarif_kg:float
    colis: Colis
    gp:GP
    
    

    id = db.Column(db.Integer(), primary_key=True)
    #date_depart = db.Column(db.DateTime(timezone=True))
    date_depart = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_arrive = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    adresse_depart= db.Column(db.String(length=64), nullable=False, unique=False)
    adresse_arrive= db.Column(db.String(length=64), nullable=False, unique=False)
    tarif_kg= db.Column(db.Float(), nullable=False, unique=False)
    nombre_kg_disponible= db.Column(db.Float(), nullable=False, unique=False)
    gp_id=db.Column(db.Integer(),db.ForeignKey('user.id'), nullable=False)
    colis = db.relationship("Colis", backref="voyage", lazy=True)
    gp = db.relationship("GP", backref="gps", lazy=True)


    def add_gp(self,id):
        self.gp_id=db.session.query(GP).filter_by(id=id).first().id
        #self.gpp=db.session.query(self).filter_by(id=self.gp_id).first().voyage
   


@dataclass
class Destinataire(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    nom= db.Column(db.String(length=32), nullable=False, unique=False)
    prenom=db.Column(db.String(length=32), nullable=False, unique=False)
    telephone=db.Column(db.String(length=32), nullable=False, unique=True)
    email=db.Column(db.String(length=32), nullable=True, unique=True)
    adresse=db.Column(db.String(length=255), nullable=True, unique=False)
@dataclass
class Livraison(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    id_colis= db.Column(db.Integer(),db.ForeignKey('colis.id'), unique=True, nullable=False)
    id_destinataire= db.Column(db.Integer(),db.ForeignKey('destinataire.id'), unique=True, nullable=False)
    date_livraison = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    payement=db.Column(db.Boolean(), nullable=False)
    livrer=db.Column(db.Boolean(), nullable=False)
@dataclass
class Payement(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    id_colis= db.Column(db.Integer(),db.ForeignKey('colis.id'), unique=True, nullable=False)
    date_payement = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    numero_transaction=db.Column(db.String(64), nullable=False, unique=True)
    statut=db.Column(db.Enum("reception", "en cours", "..."), nullable=False)
