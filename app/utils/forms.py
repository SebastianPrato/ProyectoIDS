from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = StringField("Ingrese su mail", validators=[DataRequired(message="El email es obligatorio"),
                                                        Email(message="Email inválido")])
    password = PasswordField("Ingrese su contrasena", validators=[DataRequired(message="La contrasena es obligatoria")])
    submit = SubmitField("Confirmar")
    