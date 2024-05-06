from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.json.sort_keys = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hashtag.db"
app.config["SECRET_KEY"] = "74ebfec1776062b0a3b4bea59f16e619"

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

login_manager.login_view = "login"

from consulta_clientes import routes
