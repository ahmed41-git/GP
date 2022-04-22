from api import db

from dataclasses import dataclass
from enum import unique
import enum


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

