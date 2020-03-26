#!/usr/bin/env python

import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.db import db

from app import create_app

app = create_app()
app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def deploy():
    from flask_migrate import init, migrate, upgrade
    from app.cities.models import Cities
    from app.regions.models import Regions
    from app.users.models import Users

    init()
    migrate()
    upgrade()

if __name__ == '__main__':
    manager.run()