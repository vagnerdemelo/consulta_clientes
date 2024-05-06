from consulta_clientes import database
from consulta_clientes.models import Users, Costumers

def get_one_costumer(email):
  costumer = Costumers.query.filter_by(email=email).all()

  if costumer:
    users = []

    for user in costumer:
      users.append(
        {
          "id": user.id,
          "costumer": user.costumer,
          "email": user.email,
          "status_payment": user.status_payment,
          "status_access": user.status_access
        }
      )

    return users

def get_costumers():
  costumers = Costumers.query.all()
  print(f"get costumers [{costumers}]")
  response = []
  for costumer in costumers:
    response.append(
      {
        "id": costumer.id,
        "costumer": costumer.costumer,
        "email": costumer.email,
        "status_payment": costumer.status_payment,
        "status_access": costumer.status_access
      }
    )

  return response

def access_status(status_json):
  status_access = {"aprovado": "acesso liberado", "recusado": "acesso bloqueado por falta de pagamento", "reembolsado": "acesso bloqueado"}
  status = status_access.get(status_json)
  return status

def insert_costumer(params, status_access):
  costumer = Costumers(costumer=params['nome'], email=params['email'], status_payment=params['status'], status_access=status_access)
  database.session.add(costumer)
  database.session.commit()


def update_costumer(params, status_access, email):
  costumer = Costumers.query.filter_by(email=email).first()
  costumer.costumer = params['nome']
  costumer.email = params['email']
  costumer.status_payment = params['status']
  costumer.status_access = status_access

  database.session.commit()

def email_costumer_db(email):
  costumer = Costumers.query.filter_by(email=email).first()

  if costumer:
    return costumer.email
