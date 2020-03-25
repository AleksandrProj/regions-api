import os
from flask import Flask
from .db import db, ma

def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    
    ma.init_app(app)
    db.init_app(app)

    with app.test_request_context():
        db.create_all()

    import app.regions.views as regions
    import app.cities.views as cities
    import app.users.views as users

    app.register_blueprint(regions.module)
    app.register_blueprint(cities.module)
    app.register_blueprint(users.module)

    return app