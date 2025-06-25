from flask import render_template, redirect, url_for, flash, session, request, Blueprint
from utils.forms import CategoriasForm
import requests

API_BASE = "http://localhost:5001/api"

admin_categorias_bp = Blueprint('admin_categorias', __name__)


# Funciones
def listar_categorias():
    response = requests.get(f"{API_BASE}/admin/usuario/admin/listar_categorias")
    if response.status_code == 200:
        data = response.json()
        print(data['categorias'])
        return data['categorias']
    return {}

def get_categoria(id):
    response = requests.get(f"{API_BASE}/admin/usuario/admin/categoria/{id}")
    if response.status_code == 200:
        data = response.json()
        return data
    return 


# Rutas
@admin_categorias_bp.route('/admin/categorias', methods=['GET'])
def categorias():
    if session.get('administrador') != 1:
        return redirect(url_for('home'))
    return render_template('admin/categorias.html', categorias=listar_categorias())

@admin_categorias_bp.route('/admin/categorias/eliminar/<id>', methods=['GET', 'POST'])
def eliminar_categorias(id):
    if session.get('administrador') != 1:
        return redirect(url_for('home'))
    categoria = get_categoria(id)
    nombre_categoria = categoria[1]
    categoria_id = categoria[0]

    if request.method == 'POST':
        response = requests.delete(f"{API_BASE}/admin/usuario/admin/eliminar_categoria/{id}")
        if response.status_code == 200:
            return redirect(url_for('categorias'))

    return render_template('admin/confirmacion.html',
                           nombre_categoria=nombre_categoria,
                           categoria_id=categoria_id)

@admin_categorias_bp.route('/admin/categorias/editar/<id>', methods=['GET', 'POST'])
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
        response = requests.put(f"{API_BASE}/admin/usuario/admin/editar_categoria/{id}", json=json)
        if response.status_code == 200:
            return redirect(url_for('categorias'))
    if request.method == 'GET':
        form.name.data = viejo_nombre
    return render_template('admin/confirmacion.html',
                           viejo_nombre = viejo_nombre,
                           categoria_id=categoria_id,
                           form = form)

@admin_categorias_bp.route('/admin/categorias/agregar', methods=['GET', 'POST'])
def crear_categorias():
    if session.get('administrador') != 1:
        return redirect(url_for('home'))
    form = CategoriasForm()
    if form.validate_on_submit(): 
        nombre = form.name.data
        json = {'nombre': nombre}
        response = requests.post(f"{API_BASE}/admin/usuario/admin/crear_categoria", json=json)
        if response.status_code == 201:
            return redirect(url_for('categorias'))
    return render_template('admin/confirmacion.html',
                           creacion = True,
                           form = form)
