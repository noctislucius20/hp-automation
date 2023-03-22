from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from sqlalchemy_utils.functions import database_exists, create_database
from dotenv import load_dotenv
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.wrappers import Response

import os

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)

    # DB connection variables
    pg_host = os.getenv('PGHOST')
    pg_port = os.getenv('PGPORT')
    pg_db = os.getenv('PGDATABASE')
    pg_user = os.getenv('PGUSER')
    pg_pass = os.getenv('PGPASSWORD')

    # flask app configuration
    app.config.update(
        SECRET_KEY = os.getenv('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI = f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}',
        JSON_SORT_KEYS = False,
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    )
    app.wsgi_app = DispatcherMiddleware(Response('{"resource not found"}', status=404, content_type='application/json'), {'/api/v1':app.wsgi_app})

    # checking database existence
    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        create_database(app.config['SQLALCHEMY_DATABASE_URI'])

    # app initialization
    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    # import all models for migrations
    from src.models.UsersModel import Users
    from src.models.HoneypotsModel import Honeypots
    from src.models.SensorsModel import Sensors
    from src.models.AuthenticationsModel import Authentications
    from src.models.HoneypotSensorModel import HoneypotSensor
    from src.models.HoneypotDetailsModel import HoneypotDetails
    from src.models.SensorDetailsModel import SensorDetails

    # register blueprints for route
    from src.controllers.UsersController import user
    from src.controllers.ApiInfoController import api
    from src.controllers.SensorsController import sensor
    from src.controllers.HoneypotsController import honeypot
    from src.controllers.HoneypotSensorController import honeypotsensor
    from src.controllers.JobsController import jobs

    app.register_blueprint(user)
    app.register_blueprint(api)
    app.register_blueprint(sensor)
    app.register_blueprint(honeypot)
    app.register_blueprint(honeypotsensor)
    app.register_blueprint(jobs, url_prefix='/ansible')

    return app
