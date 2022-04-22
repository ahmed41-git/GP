from dataclasses import dataclass
from enum import unique
import enum
from api import db
import api.modules.user as u
import api.modules.voyage as Voyage

@dataclass
class GP(u.User):
    categorie:enum
    voyages : Voyage

    __mapper_args__ = {'polymorphic_identity': 'gp'}
    id = db.Column(db.Integer(),db.ForeignKey('user.id'), primary_key=True)
    voyages = db.relationship("Voyage", backref="voyageur", lazy=True)
    categorie=db.Column(db.Enum("entreprise", "particulier"), nullable=False, unique=False)

