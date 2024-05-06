from consulta_clientes import database, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id_user):
  return Users.query.get(int(id_user))

class Costumers(database.Model):
  id = database.Column(database.Integer, primary_key=True)
  costumer = database.Column(database.String, nullable=False)
  email = database.Column(database.String, nullable=False, unique=True)
  status_payment = database.Column(database.String, nullable=False)
  status_access = database.Column(database.String, nullable=False)

class Users(database.Model, UserMixin):
  id = database.Column(database.Integer, primary_key=True)
  username = database.Column(database.String, nullable=False)
  email = database.Column(database.String, nullable=False, unique=True)
  password = database.Column(database.String, nullable=False)
