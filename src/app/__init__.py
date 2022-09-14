import os
from flask import Flask
from src.app.config import app_config
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from src.app.swagger import create_swagger
from flask_cors import CORS

DB = SQLAlchemy()
MA = Marshmallow()

def create_app():

  app = Flask(__name__)

  app.config.from_object(app_config[os.getenv('FLASK_ENV')])
  DB.init_app(app)
  MA.init_app(app)
  Migrate(app=app, db=DB, directory='./src/app/migrations')
  create_swagger(app)
  CORS(app)
  app.config["Access-Control-Allow-Origin"] = "*"
  app.config["Access-Control-Allow-Headers"] = "Content-Type"

  from src.app.models import technology, developer, country, state, city, user

  return app
