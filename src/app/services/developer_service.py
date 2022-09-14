from src.app.models.developer import Developer, developers_share_schema
from src.app.models.technology import technologies_share_schema

def list_all_developers_service():

  list_developers = Developer.query.all()
  list_developers_dict = developers_share_schema.dump(list_developers)


  return list_developers_dict