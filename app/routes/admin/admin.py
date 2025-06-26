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
    message = None

    if session.get('administrador') != 1:
        return redirect(url_for('public.home'))
    if request.method == "POST":
        id = request.form["producto"]
        if not id:
            message = "Debe proporcionar un ID"
            return render_template('admin/gestion.html', message=message)

        try:
            id_int = int(id)
        except ValueError:
            message = "El ID debe ser un número entero"
            return render_template('admin/gestion.html', message=message)

        producto = obtener_producto(id_int)
        if not producto:
            message = "Producto no encontrado"
            return render_template('admin/gestion.html', message=message)

        return redirect(url_for('admin_productos.modificar', id_producto=id_int))

    return render_template('admin/gestion.html')
