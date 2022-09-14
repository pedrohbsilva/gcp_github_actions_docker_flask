from datetime import datetime, timedelta
from src.app.utils import generate_jwt

from src.app.models.user import User
from src.app.models.role import Role
from src.app.models.user import User, user_share_schema


def create_user(city_id, name, age, email, password, roles):
  try:
    if roles == None:
      roles = "HELPER"

    roles_query = Role.query.filter_by(description = roles).all()

    User.seed(
      city_id,
      name, 
      age, 
      email, 
      password, 
      roles_query
    )

    return {"message": "Usuário foi criado com sucesso."}
  except:
    return {"error": "Algo deu errado!"}

def login_user(email, password):
  try:
    user_query = User.query.filter_by(email = email).first_or_404()
    user_dict = user_share_schema.dump(user_query)

    if not user_query.check_password(password):
      return { "error": "Suas credênciais estão incorretas!", "status_code": 401 }
    
    payload = {
      "user_id": user_query.id,
      "exp": datetime.utcnow() + timedelta(days=1),
      "roles": user_dict["roles"]
    }

    token = generate_jwt(payload)

    return { "token": token }

  except:
    return { "error": "Algo deu errado!", "status_code": 500 }

def get_user_by_email(email):
  try:
    user_query = User.query.filter_by(email = email).first_or_404()
    user_dict = user_share_schema.dump(user_query)
    return { "id": user_dict['id'], "roles": user_dict["roles"] }
  except:
    return { "error": "Algo deu errado!", "status_code": 500 }