from dataclasses import dataclass
from enum import unique
from datetime import date, datetime, timezone
from api import db

import api.modules.colis as c
import api.modules.gp as g

@dataclass
class Voyage(db.Model):
    date_depart:datetime
    date_arrive:datetime
    adresse_depart:str
    adresse_arrive:str
    nombre_kg_disponible:int
    tarif_kg:float
    colis: c.Colis
    gp:g.GP
    
    

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
