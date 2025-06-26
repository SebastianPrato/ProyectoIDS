from flask import render_template, redirect, url_for, flash, Blueprint
from utils.forms import RegisterForm
import requests

API_BASE = "http://127.0.0.1:5001/api"

public_usuarios_bp = Blueprint('public_usuarios', __name__)

# Rutas
@public_usuarios_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegisterForm()

    if form.validate_on_submit():
        nombre = form.name.data.strip()
        apellido = form.surname.data.strip()
        email = form.email.data
        contrasenia = form.password.data.strip()
        usuario={"nombre": nombre, "apellido": apellido, "email":email, "contrasenia":contrasenia}
        response = requests.post(f"{API_BASE}/usuarios/registro", json=usuario)
        if response.status_code == 200:
            return redirect(url_for('login'))
        else:
            flash("Hubo un error al registrar. Intenta nuevamente.") 
    return render_template('public/registro.html', form=form)

