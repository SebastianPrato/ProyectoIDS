from flask import render_template, redirect, url_for, flash, session, request, Blueprint
from utils.forms import CategoriasForm
import requests

API_BASE = "http://127.0.0.1:5001/api"

admin_bp = Blueprint('admin', __name__)

# Funciones
def obtener_producto(id):
    response = requests.get(f"{API_BASE}/productos/{id}")
    if response.status_code == 200:
        return response.json()
    return {}


# Rutas
@admin_bp.route('/', methods=['GET', 'POST'])
def home_admin():
    if session.get('administrador') != 1:
        return redirect(url_for('home'))
    if request.method == "POST":
        id = request.form["producto"]
        if not id:
            flash("Debes ingresar un ID", "warning")
            return redirect(url_for('home_admin'))

        try:
            id_int = int(id)
        except ValueError:
            flash("ID inválido", "warning")
            return redirect(url_for('home_admin'))

        producto = obtener_producto(id_int)
        if not producto:
            flash("No se encontró ningún producto con ese ID", "warning")
            return redirect(url_for('home_admin'))

        return redirect(url_for('admin_productos.modificar', id_producto=id_int))

    return render_template('admin/gestion.html')
