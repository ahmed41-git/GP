from datetime import datetime
from api import db
from api import app
from flask import render_template, jsonify
from api.models import User, Voyage, GP,Colis

"""

from dataclasses import dataclass
import api.modules.user as u
import api.modules.voyage as Voyage
import api.modules.colis as Colis
import api.modules.api as GP"""
import api.modules.fonctions as f
@app.route('/')
@app.route("/accueil")
def home_page():
    #essai = GP(nom="GUEYE", prenom='Mohamed', telephone="075823921", email="gueyemohalsdedsddk", password="passer123",categorie="entreprise")
    #voyage=Voyage()
    #db.create_all()
    #db.session.add(essai)
    #db.session.add(voyage)
    #db.session.commit()
    return jsonify(f.lister(User))


@app.route("/gp")
def gp_serealizer():
    gp = GP(nom="SALL", prenom='mOUSSA', telephone="084421SD2", email="aesyemoleSDSds00ddk", password="passer455", categorie="entreprise")
    #f.add(gp)
    return jsonify(f.lister(GP))
   
@app.route("/voyage")
def voyage_serealizer():
   
    voyage=Voyage(adresse_depart="Mali", adresse_arrive="CANDA", tarif_kg=20, nombre_kg_disponible=30)
    voyage.add_gp(1)
    f.add(voyage)

    return jsonify(f.lister(Voyage))
@app.route("/colis") 
def colis_serealizer():
    colis=Colis(type_colis="type11", forme="forme1", poids=20)
    #oyage.add_gp(3)
    f.add(colis)
    return jsonify(f.lister(Colis))
@app.route("/Users")
def detailGP():
    return jsonify([*map(gp_serealizer, User.query.all())])