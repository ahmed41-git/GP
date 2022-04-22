from api import db
from api.models import Voyage
from datetime import datetime
def add(objet):
    db.create_all()
    db.session.add(objet)
    db.session.commit()


def delete(objet):
    db.session.delete(objet)
    db.session.commit()
def lister(objet):
    return objet.query.all()

def rechercher_date(date):
        return db.session.query(Voyage).filter(Voyage.date_depart > date)

