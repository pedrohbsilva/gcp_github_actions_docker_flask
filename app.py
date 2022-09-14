from src.app import create_app
from src.app.routes import routes
from flask.cli import with_appcontext
import click
from src.app.db import populate_db
from src.app import DB

from src.app.db import populate_db
from src.app import DB
app = create_app()
routes(app)

@click.command(name='populate_db')#Comando para popular o banco de dados
@with_appcontext #Verificação no flask, que identifica o comando que executará a função abaixo.
def call_command():
  populate_db()

@click.command(name='delete_tables') #Comando para deletar as tabelas do banco de dados
@with_appcontext #Verificação no flask, que identifica o comando que executará a função abaixo.
def delete_tables():
  DB.drop_all()

app.cli.add_command(call_command)#Adicionar na instanciação do Flask para encontrar o comando.
app.cli.add_command(delete_tables)#Adicionar na instanciação do Flask para encontrar o comando.


if __name__ == "__main__":
  app.run()