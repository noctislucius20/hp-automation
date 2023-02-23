from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from sqlalchemy_utils.functions import database_exists, create_database
from dotenv import load_dotenv

import os

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()

def create_app():
    app = Flask(__name__)

    # DB connection variables
    pg_host = os.getenv('PGHOST')
    pg_port = os.getenv('PGPORT')
    pg_db = os.getenv('PGDATABASE')
    pg_user = os.getenv('PGUSER')
    pg_pass = os.getenv('PGPASSWORD')

    # flask app configuration
    app.config = {
        'SECRET_KEY': os.getenv('SECRET_KEY'),
        'JSON_SORT_KEYS': False,
        'SQLALCHEMY_DATABASE_URI': f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}',
        'TEMPLATES_AUTO_RELOAD' : True
    }

    # checking database existence
    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        create_database(app.config['SQLALCHEMY_DATABASE_URI'])

    # app initialization
    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    return app
