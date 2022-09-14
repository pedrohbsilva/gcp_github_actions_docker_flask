from flask import Flask
from src.app.controllers.technologies import technology
from src.app.controllers.developers import developers
from src.app.controllers.cities import cities
from src.app.controllers.users import user

def routes(app: Flask):
  app.register_blueprint(technology)
  app.register_blueprint(developers)
  app.register_blueprint(cities)
  app.register_blueprint(user)