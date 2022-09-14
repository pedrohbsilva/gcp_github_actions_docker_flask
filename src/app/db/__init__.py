from flask import json
from sqlalchemy.sql.expression import func
import requests
from src.app.models.city import City, cities_share_schema
from src.app.models.developer import Developer
from src.app.models.state import State, states_share_schema
from src.app.models.country import Country, country_share_schema
from src.app.models.user import User, users_share_schema
from src.app.models.technology import Technology
from src.app.models.role import Role
from src.app.models.permission import Permission

def save(data, db_name): 
    json_object = json.dumps(data, indent=4)
    with open(f'src/app/db/{db_name}.json', 'w') as outFile:
      outFile.write(json_object)

def read(db_name):
  try:
    with open(f'src/app/db/{db_name}.json', 'r') as openFile:
      json_object = json.load(openFile)
      return json_object

  except:
    return None

def populate_db():

  country = Country.query.first()

  if country != None:
    print('Já existe dados populados.')
    return
  brasil_code = 76
  countries_data = requests.get(f"https://servicodados.ibge.gov.br/api/v1/localidades/paises/{brasil_code}")
  states_data = requests.get("https://servicodados.ibge.gov.br/api/v1/localidades/estados")
  cities_data = requests.get("https://servicodados.ibge.gov.br/api/v1/localidades/municipios")

  country_name = countries_data.json()[0]['nome']
  Country.seed(country_name, 'Português') # Seed utilizada para salvar dados

  country = Country.query.first() # Query para verificar se existe dados salvos
  country_dict = country_share_schema.dump(country) # Método para serializar o dado

  for stateObject in states_data.json(): # For para criar dados em massa dos estados
    State.seed(
      country_dict['id'],
      stateObject['nome'],
      stateObject['sigla']
    )

  state = State.query.order_by(State.name.asc()).all()
  state_dict = states_share_schema.dump(state)

  for city_object in cities_data.json():
    state_id = 0
    for state_object in state_dict:
      if state_object['initials'] == city_object['microrregiao']['mesorregiao']['UF']['sigla']:
        state_id = state_object['id']
    City.seed(
      state_id,
      city_object['nome']
    )

  cities = City.query.order_by(City.name.asc()).all()
  cities_dict = cities_share_schema.dump(cities)

  users = requests.get('https://randomuser.me/api?nat=br&results=100')
  techs = requests.get('https://lit-citadel-12163.herokuapp.com/technologies/get_all_technologies')

  permissions = ['DELETE', 'READ', 'WRITE', 'UPDATE']
  roles = ['OWNER', 'HELPER']

  for permission in permissions:
    Permission.seed(
      permission
    )
    
  permissions_helper = Permission.query.filter(
    Permission.description.in_([
      'READ', 'WRITE'
    ])
  ).all()

  permissions_owner = Permission.query.all()

  for index, role in enumerate(roles):
    if index == 0:
      Role.seed(
        role,
        permissions_owner
      )
    else:
      Role.seed(
        role,
        permissions_helper
      )

  for tech_object in techs.json():
    Technology.seed(
      tech_object['name']
    )

  roles_query = Role.query.filter_by(description = "HELPER").all()
  for user in users.json()['results']:
    city_id = 2
    for city_object in cities_dict:
      if user['location']['city'] == city_object['name']:
        city_id = city_object['id']
    User.seed(
      city_id,
      user['name']['first'] + ' ' + user['name']['last'],
      user['registered']['age'],
      user['email'],
      user['login']['password'],
      roles_query
    )

  users = User.query.order_by(User.name.asc()).all()
  users_dict = users_share_schema.dump(users)

  for index, user_object in enumerate(users_dict):
    if index % 2 == 0: # if para verificar se o index é par
      techs = Technology.query.order_by(func.random()).limit(10).all() # query que retorna aleatóriamente 10 tecnologias
      Developer.seed(
        None,
        index % 2 == 0,
        user_object['id'],
        techs
      )
  print("Dados inseridos com sucesso.")
  return
