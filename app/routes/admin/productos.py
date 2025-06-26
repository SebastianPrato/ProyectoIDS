from flask import render_template, redirect, url_for, flash, session, request, Blueprint
from utils.forms import CategoriasForm
import requests

from routes.public.productos import listar_categorias

API_BASE = "http://127.0.0.1:5001/api"

admin_productos_bp = Blueprint('admin_productos', __name__)


# Funciones
def obtener_producto(id):
    response = requests.get(f"{API_BASE}/productos/{id}")
    if response.status_code == 200:
        return response.json()
    return {}

def cargar_producto(producto):
    response=requests.post(f"{API_BASE}/admin/cargar", json=producto)
    if response.status_code==201:
        return True
    return False

def gestionar_stock(producto, id):
    response=requests.post(f"{API_BASE}/admin/modificar/{id}", json=producto)
    if response.status_code==201:
        return True
    return False

# Rutas
@admin_productos_bp.route('/modificar/<int:id_producto>', methods=['GET', 'POST']) #cumple lo basico
def modificar(id_producto):
    message = None

    if session.get('administrador') != 1:
        return redirect(url_for('public.home'))
    juego=obtener_producto(id_producto)
    if request.method== "POST":
        producto_m=request.form
        ok=gestionar_stock(producto_m, id=id_producto)

        if not ok:
            message = "Error al modificar producto"
        else:
            message = "Producto modificado con éxito"
            return redirect(url_for('admin.home_admin'))
    
    categorias = listar_categorias()
    return render_template('admin/modificar.html', producto=juego, modificar= True, categorias=categorias, message=message)

@admin_productos_bp.route('/cargar', methods=['GET', 'POST']) 
def cargar():
    message = None

    if session.get('administrador') != 1:
        return redirect(url_for('public.home'))
    if request.method== "POST":
        producto=request.form
        ok=cargar_producto(producto)
        if not ok:
            message = "Error al cargar producto"
        else:
            message = "Producto cargado con éxito"
            return redirect(url_for('admin.home_admin'))

    categorias = listar_categorias() 
    return render_template('admin/modificar.html', producto={}, modificar= False, categorias=categorias, message=message)
