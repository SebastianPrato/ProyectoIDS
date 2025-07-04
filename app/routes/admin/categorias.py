from flask import render_template, redirect, url_for, flash, session, request, Blueprint
from utils.forms import CategoriasForm
import requests
from routes.public.productos import listar_categorias

API_BASE = "http://127.0.0.1:5001/api"

admin_categorias_bp = Blueprint('admin_categorias', __name__)


# Funciones
def get_categoria(id):
    response = requests.get(f"{API_BASE}/admin/categorias/{id}")
    if response.status_code == 200:
        data = response.json()
        return data
    return 

def obtener_productos_categoria(id_categoria):
    response=requests.get(f"{API_BASE}/productos/categoria/{id_categoria}")
    if response.status_code==200:
        return response.json()
    return {}


# Rutas
@admin_categorias_bp.route('/categorias', methods=['GET'])
def categorias():
    if session.get('administrador') != 1:
        return redirect(url_for('public.home'))
    return render_template('admin/categorias.html', categorias=listar_categorias())

@admin_categorias_bp.route('/categorias/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar_categorias(id):
    if session.get('administrador') != 1:
        return redirect(url_for('home'))
    categoria = get_categoria(id)
    print(categoria)
    nombre_categoria = categoria[1]
    categoria_id = categoria[0]
    productos_asignados = obtener_productos_categoria(id)
    existen_productos = False
    if len(productos_asignados) == 0:
        existen_productos = True

    if request.method == 'POST' and existen_productos:
        response = requests.delete(f"{API_BASE}/admin/eliminar_categoria/{id}")
        if response.status_code == 200:
            return redirect(url_for('admin_categorias.categorias'))

    return render_template('admin/confirmacion.html',
                           nombre_categoria=nombre_categoria,
                           categoria_id=categoria_id,
                           existen_productos = existen_productos,
                           productos_asignados = productos_asignados)

@admin_categorias_bp.route('/categorias/editar/<int:id>', methods=['GET', 'POST'])
def editar_categorias(id):
    if session.get('administrador') != 1:
        return redirect(url_for('home'))
    form = CategoriasForm()
    categoria = get_categoria(id)
    viejo_nombre = categoria[1]
    categoria_id = categoria[0]

    if form.validate_on_submit(): 
        nombre = form.name.data
        json = {'nombre': nombre}
        response = requests.put(f"{API_BASE}/admin/editar_categoria/{id}", json=json)
        if response.status_code == 200:
            return redirect(url_for('admin_categorias.categorias'))
    if request.method == 'GET':
        form.name.data = viejo_nombre
    return render_template('admin/confirmacion.html',
                           viejo_nombre = viejo_nombre,
                           categoria_id=categoria_id,
                           form = form)

@admin_categorias_bp.route('/categorias/agregar', methods=['GET', 'POST'])
def crear_categorias():
    if session.get('administrador') != 1:
        return redirect(url_for('home'))
    form = CategoriasForm()
    if form.validate_on_submit(): 
        nombre = form.name.data
        json = {'nombre': nombre}
        response = requests.post(f"{API_BASE}/admin/crear_categoria", json=json)
        if response.status_code == 201:
            return redirect(url_for('admin_categorias.categorias'))
    return render_template('admin/confirmacion.html',
                           creacion = True,
                           form = form)
