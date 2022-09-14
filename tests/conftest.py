import pytest
from src.app import create_app
from src.app.routes import routes


@pytest.fixture(scope="module")
def app():
  """
    Instance of app
  """

  app_on = create_app()
  routes(app_on)
  return app_on