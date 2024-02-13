from flask import request, jsonify
from flask_restx import Resource
from flask_jwt_extended import create_access_token
from config import app
from flask_restx import Resource, Namespace, fields
from flask_restx import reqparse
from models import *
from werkzeug.security import generate_password_hash, check_password_hash

auth_namespace = Namespace('auth', description='Endpoints pour les films')
auth_model = auth_namespace.model('Auth', {
    'username': fields.String(description='Nom utilisateur'),
    'password': fields.String(description='Mot de passe'),
})

user_model = auth_namespace.model('UserModel', {
    'id': fields.Integer(),
    'username': fields.String(description='Nom utilisateur'),
    
})

@auth_namespace.route("/register")
class Register(Resource):

    @auth_namespace.expect(auth_model)
    @auth_namespace.marshal_with(user_model)
    def post(self):
        user = User(username = auth_namespace.payload["username"], password=generate_password_hash(auth_namespace.payload["password"]))
        db.session.add(user)
        db.session.commit()
        return user

@auth_namespace.route("/login")
class Login(Resource):
    @auth_namespace.expect(auth_model)
    def post(self):
        user = User.query.filter_by(username = auth_namespace.payload["username"]).first()
        if not user:
            return {"error":"user doesn't exist"}
        if not check_password_hash(user.password, auth_namespace.payload["password"]):
            return {"error": "Incorrect password"}
        return {"token": create_access_token(user.username)}