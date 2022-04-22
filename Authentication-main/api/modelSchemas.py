from flask import Flask
from api.models import User, Admin
from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from api import ma



class AdminSchema(SQLAlchemySchema):
    class Meta:
        model = Admin
        load_instance = True

    id = fields.Str()
    nom = fields.Str()
    prenom = fields.Str()


class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    id = fields.Str()
    numero_telephone = fields.Str()
    email = fields.Str()
    discriminator = fields.Str()