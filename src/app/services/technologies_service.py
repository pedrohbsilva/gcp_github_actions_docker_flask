from src.app.utils import exist_key, exist_value
from flask import jsonify
from src.app.db import save, read

def create_new_technlogy(json, keys):
  data = exist_key(json, keys)

  if 'error' in data:
    return jsonify(data)
  
  techs = read('technologies')

  if techs == None or len(techs) == 0:
    save([data], 'technologies')
    return jsonify(data)

  if exist_value(data, techs):
    return jsonify({"error": "Algum dos items que foi enviado, já existe no banco de dados"})

  techs.append(data)
  save(techs, 'technologies')

  return jsonify(techs)
