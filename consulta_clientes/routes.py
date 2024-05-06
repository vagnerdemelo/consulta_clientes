from flask import render_template, url_for, redirect,request, jsonify, make_response
from consulta_clientes import app, database, bcrypt
from consulta_clientes.modules import *
from consulta_clientes.models import Users, Costumers
from flask_login import login_required, login_user,logout_user
from consulta_clientes.forms import FormLogin, FormSignup

@app.route('/', methods=['GET', 'POST'])
def login():
  form_login = FormLogin()
  if form_login:
    user = Users.query.filter_by(email=form_login.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form_login.password.data):
      login_user(user)
      return redirect(url_for("user", username=user.username))
  return render_template('login.html', form=form_login)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form_signup = FormSignup()
  if form_signup.validate_on_submit():
    user_token = "uhdfaAADF123"
    token = form_signup.token.data
    if token == user_token:
      password = bcrypt.generate_password_hash(form_signup.password.data)
      user = Users(username=form_signup.username.data, email=form_signup.email.data, password=password)

      database.session.add(user)
      database.session.commit()
      # database.session.close()
      login_user(user, remember=True)
      return redirect(url_for("user", username=user.username))

  return render_template('signup.html', form=form_signup)

@app.route('/user/<username>', methods=['GET'])
@login_required
def user(username):
  return render_template('user.html', username=username)

@app.route('/processar_consulta', methods=['POST'])
def processar_consulta():
  termo_busca = request.form['termo_busca']
  tipo_busca = request.form['tipo_busca']

  if tipo_busca == 'email':
    costumers = get_one_costumer(termo_busca)
  else:
    costumers = get_costumers()
    print(costumers)

  html_resultados = "<table><tr><th>ID</th><th>Cliente</th><th>Email</th><th>Status de Pagamento</th><th>Status de Acesso</th></tr>"
  for costumer in costumers:
      html_resultados += f"<tr><td>{costumer['id']}</td><td>{costumer['costumer']}</td><td>{costumer['email']}</td><td>{costumer['status_payment']}</td><td>{costumer['status_access']}</td></tr>"
  html_resultados += "</table>"

  return jsonify(html_resultados)

@app.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect('/')

# rota que a api recebe o costumer
@app.route('/costumer', methods=['POST'])
def create_costumer():
  params = request.json
  status_access = access_status(params['status'])
  email_db = email_costumer_db(params['email'])

  if params['email'] == email_db:
    update_costumer(params, status_access, email_db)
  else:
    insert_costumer(params, status_access)

  return make_response(
    jsonify(
      message = "User has been created successfully.",
      costumer = params
      )
    )
