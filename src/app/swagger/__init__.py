from flasgger import Swagger
from flask import Flask

def create_swagger(app: Flask):
  app.config['SWAGGER'] = {
    'openapi': '3.0.0',
    'title': 'Info Api',
    'description': "Aplicação de dados sobre desenvolvedores"
  }

  Swagger(app)