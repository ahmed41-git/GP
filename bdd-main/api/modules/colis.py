from api import db
import api.modules.voyage as Voyage
import api.modules.gp as g

from datetime import datetime
import enum

from dataclasses import dataclass

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
        self.gp_id=db.session.query(g.GP).filter_by(id=id).first().id