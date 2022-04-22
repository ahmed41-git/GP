from flask import render_template, request, flash, jsonify, redirect, url_for,json
from werkzeug.security import generate_password_hash
from api.models import User, Admin, Client, Livreur,Livraison,Paiement
from api import db
from api import app

db.create_all()

def users_serializer(user):
    return {
        'id': user.id,
        'type': user.discriminator,
        'numero_telephone': user.numero_telephone,
        'email': user.email
    }

def admins_serializer(admin):
    return {
        'id': admin.id,
        'nom': admin.nom,
        'prenom' : admin.prenom,
        'email': admin.email
    }

def clients_serializer(client):
    return {
        'id': client.id,
        'nom': client.nom,
        'prenom' : client.prenom,
        'email': client.email
    }

def livreurs_serializer(livreur):
    return {
        'id': livreur.id,
        'nom': livreur.nom,
        'prenom' : livreur.prenom,
        'email': livreur.email
    }


@app.route('/')
def index():
    json_com={
            'test': 'testAPI'
        }
    
    reponse = jsonify({"test":json_com})

    return reponse.json


@app.route('/api/listeUsers')
def getUsers():
    return jsonify([*map(users_serializer, User.query.all())])



@app.route('/api/listeAdmins')
def getAdmins():
    return jsonify([*map(admins_serializer, Admin.query.all())])


@app.route('/api/listeClients')
def getClients():
    return jsonify([*map(clients_serializer, Client.query.all())])


@app.route('/api/listeLivreurs')
def getLivreurs():
    return jsonify([*map(livreurs_serializer, Livreur.query.all())])


@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

   # new_user = User(numero_telephone=data['numero_telephone'], email=data['email'], password=hashed_password, discriminator=data['type'])
    
    if(data['type'] == "admin"):
        new_admin = Admin(numero_telephone=data['numero_telephone'], email=data['email'], password=hashed_password, discriminator=data['type'], nom=data['nom'], prenom=data['prenom'])
        db.session.add(new_admin)

    elif(data['type'] == "client"):
        new_client = Client(numero_telephone=data['numero_telephone'], email=data['email'], password=hashed_password, discriminator=data['type'], nom=data['nom'], prenom=data['prenom'])
        db.session.add(new_client)

    elif(data['type'] == "livreur"):
        new_livreur = Livreur(numero_telephone=data['numero_telephone'], email=data['email'], password=hashed_password, discriminator=data['type'], nom=data['nom'], prenom=data['prenom'], img=data['img'])
        db.session.add(new_livreur)

    
    db.session.commit()

    return jsonify({'message' : 'New user created!'})


@app.route('/api/payer/<idLivraison>',methods=['POST'])
def payer(idLivraison):
    p = request.get_json()
    pa = Paiement(idLivraison=idLivraison,date=p['date'],statut=0)
    db.session.add(pa)
    db.session.commit()

    json_p = {
        'message': 'paiement réussi',
    }

    response = jsonify({"pa":json_p})

    return response.json


@app.route('/api/validerLivraison/client',methods=['GET'])
def validerLivraisonClient():
    #u = User.query.get(idUser) // idUser va être la suite du chemin
    livraisons = Livraison.query.all()

    table_livraisons = []
    for livraison in livraisons:
        json_com = {
            'voyage': livraison.idVoyage,
            'colis': livraison.idColis,
            'destinataire': livraison.idDestinataire,
            'dateLivraison': livraison.date,
            'paiement': livraison.paiement,
            'livraison': livraison.livraison
        }
        table_livraisons.append(json_com)

    response = jsonify({'livraisons': table_livraisons})

    return response.json

@app.route('/api/validerLivraison/client/<idLivraison>',methods=['GET'])
def validerLivraisonClientP(idLivraison):
    livr = Livraison.query.get(idLivraison)
    livr.livraison = 1
    livr.paiement = 1
    db.session.commit()

    json_p = {
        'message': "livraison validée"
    }

    response = jsonify({"pa":json_p})

    return response.json



@app.route('/api/validerLivraison/livreur',methods=['GET'])
def validerLivraisonLivreur():
    #u = User.query.get(idUser) // idUser va être la suite du chemin
    livraisons = Livraison.query.all()

    table_livraisons = []
    for livraison in livraisons:
        json_com = {
            'voyage': livraison.idVoyage,
            'colis': livraison.idColis,
            'destinataire': livraison.idDestinataire,
            'dateLivraison': livraison.date,
            'paiement': livraison.paiement,
            'livraison': livraison.livraison
        }
        table_livraisons.append(json_com)

    response = jsonify({'livraisons': table_livraisons})

    return response.json


@app.route('/api/validerLivraison/livreur/<idLivraison>',methods=['GET'])
def validerLivraisonLivreurP(idLivraison):
    livr = Livraison.query.get(idLivraison)
    livr.livraison = 2
    db.session.commit()

    json_p = {
        'message': "livraison validée"
    }

    response = jsonify({"pa":json_p})

    return response.json

