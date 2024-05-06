from consulta_clientes import database, app
from consulta_clientes.models import Costumers, Users


with app.app_context():
  database.create_all()
