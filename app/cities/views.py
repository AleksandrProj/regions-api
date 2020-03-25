from flask import Blueprint, current_app, abort, request, jsonify
from flask_restful import Api, Resource
from sqlalchemy.exc import SQLAlchemyError

from .models import Cities, CitiesSchema, db
from app.users.models import Users
from app.auth import auth_token

module = Blueprint('api_cities', __name__, url_prefix='/api/cities')
api = Api(module)

def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)

@auth_token.verify_token
def verify_token(token):
    user_token = Users.verify_auth_token(token)
    if not user_token:
        return False
    return True

# Модуль вывода городов
class AllCities(Resource):
    @auth_token.login_required
    def get(self):
        region_id_q = request.args.get('region_id')

        if region_id_q is not None:
            cities = Cities.query.filter_by(region_id=region_id_q).order_by(Cities.id).all()
        else:
            cities = Cities.query.order_by(Cities.id).all()
            
        cities_schema = CitiesSchema(many=True)
        output = cities_schema.dump(cities)
        
        return jsonify({'cities': output})

# Модуль добавление городов
class AddCities(Resource):
    @auth_token.login_required
    def post(self):
        city = Cities(
            name=request.args.get('name_city'), 
            region_id=request.args.get('region_id')
        )
        db.session.add(city)

        try:
            db.session.commit()
            return {
                'status': 'ok',
                'message': 'City successfully added'
            }, 201
        except SQLAlchemyError as e:
            log_error('Error while querying database', exc_info=e)
            return {
                'status': 'error'
            }, 500

# Модуль изменения городов
class EditCities(Resource):
    @auth_token.login_required
    def put(self):
        name_city_q = request.args.get('name_city')
        new_name_city_q = request.args.get('new_name_city')

        if name_city_q is not None and new_name_city_q is not None:
            city_field = Cities.query.filter_by(name=name_city_q).first()
            city_field.name = new_name_city_q
        else:
            return {
                'status': 'error',
                'message': 'Empty values transmitted'
            }, 400

        try:
            db.session.add(city_field)
            db.session.commit()
            return {
                'status': 'ok'
            }, 200
        except SQLAlchemyError as e:
            log_error('Error while querying database', exc_info=e)
            return {
                'status': 'error',
                'message': 'There\'s been a malfunction with the change'
            }, 500

# Модуль удаления городов
class DeleteCities(Resource):
    @auth_token.login_required
    def delete(self):
        name_city_q = request.args.get('name_city')

        if name_city_q is not None:
            Cities.query.filter_by(name=name_city_q).delete()
        else:
            return {
                'status': 'error',
                'message': 'Empty values transmitted'
            }, 400
        
        try:
            db.session.commit()
            return {
                'status': 'ok'
            }, 200
        except SQLAlchemyError as e:
            log_error('Error while querying database', exc_info=e)
            return {
                'status': 'error',
                'message': 'There was a malfunction on the removal'
            }, 500

api.add_resource(AllCities, '/')
api.add_resource(AddCities, '/add')
api.add_resource(EditCities, '/edit')
api.add_resource(DeleteCities, '/delete')
