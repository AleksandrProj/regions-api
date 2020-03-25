from flask import Blueprint, current_app, abort, request, jsonify
from flask_restful import Api, Resource
from sqlalchemy.exc import SQLAlchemyError

from .models import Regions, RegionsSchema, db
from app.users.models import Users
from app.auth import auth_token

module = Blueprint('api_regions', __name__, url_prefix='/api/regions')
api = Api(module)

def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)

@auth_token.verify_token
def verify_token(token):
    user_token = Users.verify_auth_token(token)
    if not user_token:
        return False
    return True
    

# Модуль вывода регионов
class AllRegions(Resource):
    @auth_token.login_required
    def get(self):
        regions = Regions.query.order_by(Regions.id).all()
        region_schema = RegionsSchema(many=True)
        output = region_schema.dump(regions)
        
        return jsonify({'regions': output})
        
# Модуль добавления регионов
class AddRegions(Resource):
    @auth_token.login_required
    def post(self):
        region_field = Regions(
            name=request.json.get('name_region'),
            parent_id=request.json.get('region_id')
        )
        db.session.add(region_field)

        try:
            db.session.commit()
            return {
                'status': 'ok',
                'message': 'Region successfully added'
            }, 201
        except SQLAlchemyError as e:
            log_error('Error while querying database', exc_info=e)

            return { 'status': 'error' }

# Модуль изменения регионов
class EditRegions(Resource):
    @auth_token.login_required
    def put(self):
        region_id_q = request.json.get('region_id')
        new_name_region_q = request.json.get('new_name_region')

        if region_id_q is not None or new_name_region_q is not None:
            region_field = Regions.query.filter_by(parent_id=region_id_q).first()
            region_field.name = new_name_region_q
        else:
            return {
                'status': 'error',
                'message': 'Empty values transmitted'
            }, 400

        try:
            db.session.add(region_field)
            db.session.commit()

            return { 
                'status': 'ok' 
            }, 200
        except SQLAlchemyError as e:
            log_error('Error while querying database', exc_info=e)
            return {
                'status': 'error',
                'message': 'There\'s been a malfunction with the change'
            }

# Модуль удаления регионов
class DeleteRegions(Resource):
    @auth_token.login_required
    def delete(self):
        name_region_q = request.json.get('name_region')
        region_id_q = request.json.get('region_id')

        if name_region_q is not None:
            Regions.query.filter_by(name=request.json.get('name_region')).delete()
        elif region_id_q is not None:
            Regions.query.filter_by(parent_id=request.json.get('region_id')).delete()
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

api.add_resource(AllRegions, '/')
api.add_resource(AddRegions, '/add')
api.add_resource(EditRegions, '/edit')
api.add_resource(DeleteRegions, '/delete')

