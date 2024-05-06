from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from consulta_clientes.models import Users

class FormLogin(FlaskForm):
  email = StringField("E-mail", validators=[DataRequired(), Email()])
  password = PasswordField("Senha", validators=[DataRequired()])
  submit = SubmitField("Fazer Login")
  def validate_email(self, email):
    user = Users.query.filter_by(email=email.data).first()
    if not user:
        raise ValidationError("E-mail disponivel.")

class FormSignup(FlaskForm):
  username = StringField("Nome de usuario", validators=[DataRequired()])
  email = StringField("E-mail", validators=[DataRequired(), Email()])
  password = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
  confirm_password = PasswordField("Confirmação de senha", validators=[DataRequired(), EqualTo("password")])
  token = StringField("Token", validators=[DataRequired()])
  submit = SubmitField("Criar conta")
  def validate_email(self, email):
    user = Users.query.filter_by(email=email.data).first()
    if user:
        raise ValidationError("E-mail já cadastrado, faça login para continuar.")
