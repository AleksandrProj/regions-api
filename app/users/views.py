from flask import Blueprint, current_app, abort, request, jsonify, g
from flask_restful import Api, Resource
from .models import Users, db

from app.auth import auth_password

module = Blueprint('api_users', __name__, url_prefix='/api/users')
api = Api(module)

@auth_password.verify_password
def verify_password(username_or_token, password):
    user = Users.verify_auth_token(username_or_token)
    if not user:
        user = Users.query.filter_by(login=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

class RegisterUsers(Resource):
    def post(self):
        username_q = request.json.get('username')
        password_q = request.json.get('password')

        if username_q is None or password_q is None:
            abort(400)
        if Users.query.filter_by(login=username_q).first() is not None:
            abort(400)
        
        user = Users(login=username_q)
        user.hash_password(password_q)

        db.session.add(user)
        db.session.commit()

        return jsonify({ 'username': user.login })

# Модуль получения токена
class GetAuthToken(Resource):
    @auth_password.login_required
    def get(self):
        token = g.user.generate_auth_token()
        return jsonify({ 'token': token.decode('ascii') })

api.add_resource(GetAuthToken, '/token')
api.add_resource(RegisterUsers, '/register')