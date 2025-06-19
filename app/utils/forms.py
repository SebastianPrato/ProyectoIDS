from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    email = StringField("Ingrese su mail", validators=[DataRequired(message="El email es obligatorio"),
                                                        Email(message="Email inválido")])
    password = PasswordField("Ingrese su contrasena", validators=[DataRequired(message="La contrasena es obligatoria")])
    submit = SubmitField("Confirmar")


class RegisterForm(FlaskForm):
    name = StringField("Ingrese su nombre", validators=[DataRequired(message="El nombre es obligatorio"), Length(min=3, max=15, message="El nombre debe tener entre 3 y 15 caracteres")])
    surname = StringField("El apellido es obligatorio", validators=[DataRequired(message="El apellido es obligatorio"), Length(min=3, max=15, message="El apellido debe tener entre 3 y 15 caracteres")])
    email = StringField("Ingrese su email", validators=[DataRequired(message="El email es obligatorio"),
                                                        Email(message="Email inválido")])
    password = PasswordField("Ingrese su contrasena", validators=[DataRequired(message="La contrasena es obligatoria"), Length(min=6, max=12, message="La contrasena debe tener entre 6 y 12 caracteres"), EqualTo('confirm', message="Las contrasenas deben coincidir")])
    confirm = PasswordField("Confirme su contrasena", validators=[DataRequired(message="Debe confirmar su contrasena")])
    submit = SubmitField("Confirmar")
    