from flask import json, render_template, jsonify, request, flash, jsonify, redirect, url_for, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth
import jwt
import datetime
from functools import wraps
from api.models import User, Admin, Client, Livreur
from api.modelSchemas import UserSchema, AdminSchema
from api import db
from api import app


def users_serializer(user):
    user_schema = UserSchema() 
    return user_schema.dump(user)


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
        'email': client.email,
        'numero telephone': client.numero_telephone,
        'type': client.__mapper_args__['polymorphic_identity']
    }

def livreurs_serializer(livreur):
    return {
        'id': livreur.id,
        'nom': livreur.nom,
        'prenom' : livreur.prenom,
        'email': livreur.email,
        'numero telephone': livreur.numero_telephone,
        'type': livreur.__mapper_args__['polymorphic_identity']
    }

# AUTHORIZATION
#
#
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


def user_is_admin(current_user):
    if not current_user.discriminator == "admin":
        return jsonify({'message': "You are not admin"})


@app.route('/')
def index():
    json_com={
            'test': 'testAPI'
        }
    
    reponse = jsonify({"test":json_com})

    return reponse.json


# LISTING ROUTES
# 
#  
@app.route('/api/listeUsers')
@token_required
def getUsers(current_user):

    user_is_admin(current_user)

    return jsonify([*map(users_serializer, User.query.all())])


@app.route('/api/listeAdmins')
@token_required
def getAdmins(current_user):

    user_is_admin(current_user)
    return jsonify([*map(admins_serializer, Admin.query.all())])


@app.route('/api/listeClients')
@token_required
def getClients(current_user):

    user_is_admin(current_user)
    return jsonify([*map(clients_serializer, Client.query.all())])


@app.route('/api/listeLivreurs')
@token_required
def getLivreurs(current_user):

    user_is_admin(current_user)
    return jsonify([*map(livreurs_serializer, Livreur.query.all())])


#LISTING BY ONE ROUTES
#
#
@app.route('/api/user/<id>', methods=['GET'])
def get_one_user(id):
    
    user = User.query.filter_by(id=id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    user_data = {}
    user_data['id'] = user.id
    user_data['numero_telephone'] = user.numero_telephone
    user_data['email'] = user.email
    user_data['type'] = user.__mapper_args__['polymorphic_identity'] 

    return jsonify({'user' : user_data})


@app.route('/api/client/<id>', methods=['GET'])
@token_required
def get_one_client(current_user, id):

    user_is_admin(current_user)

    client = Client.query.filter_by(id=id).first()

    if not client:
        return jsonify({'message' : 'No user found!'})

    client_data = clients_serializer(client)

    return jsonify({'user' : client_data})


@app.route('/api/livreur/<id>', methods=['GET'])
@token_required
def get_one_livreur(id):


    livreur = Livreur.query.filter_by(id=id).first()

    if not livreur:
        return jsonify({'message' : 'No user found!'})

    livreur_data = clients_serializer(livreur)

    return jsonify({'user' : livreur_data})


@app.route('/api/admin/<id>', methods=['GET'])
@token_required
def get_one_admin(current_user, id):

    user_is_admin(current_user)

    admin = Admin.query.filter_by(id=id).first()

    if not admin:
        return jsonify({'message' : 'No user found!'})

    admin_data = clients_serializer(admin)

    return jsonify({'user' : admin_data})

#USER CREATION ROUTE
#
# or registration

@app.route('/api/user', methods=['POST'])
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

#USER DELETION ROUTE
#
#
@app.route('/api/user', methods=['DELETE'])
@token_required
def delete_user(current_user, id):

    user_is_admin(current_user)

    user = User.query.filter_by(id=id).first()
    
    if not user:
        return jsonify({'user' : "No user found"})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message' : 'New user created!'})


# LOGIN ROUTE
#
#
@app.route('/api/login', methods=['POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(numero_telephone=auth.username).first()

    if not user:
        return make_response('Verifiez votre numero de telephone', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'id' : user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({ 'token': token})
        return jsonify({'token' : token.decode('UTF-8')})
        return jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

    return make_response('Mots de passes non identiques', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})