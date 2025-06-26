from flask import render_template, redirect, url_for, flash, session, request, Blueprint
from utils.forms import CategoriasForm
import requests

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
    if session.get('administrador') != 1:
        return redirect(url_for('home'))
    juego=obtener_producto(id_producto)
    if request.method== "POST":
        nombre=request.form["nombre"]
        categoria=request.form["categoria"]
        descripcion=request.form["descripcion"]
        precio=request.form["precio"]
        imagen=request.form["imagen"]
        stock=request.form["stock"]
        producto_m={"nombre": nombre, "categoria": categoria, "descripcion": descripcion, "precio": precio, "imagen": imagen, "stock": stock, "crear":False}
        ok=gestionar_stock(producto_m, id=id_producto)
        if not ok:
            flash("Error al guardar producto", "error")
        else:
            flash("Producto modificado con éxito", "success")
        return render_template("admin/modificar.html", producto=juego['id_producto'], modificar=True) 
    return render_template('admin/modificar.html', producto=juego, modificar= True )

@admin_productos_bp.route('/cargar', methods=['GET', 'POST']) 
def cargar():
    if session.get('administrador') != 1:
        return redirect(url_for('home'))
    if request.method== "POST":
        nombre=request.form["nombre"]
        categoria=request.form["categoria"]
        descripcion=request.form["descripcion"]
        precio=request.form["precio"]
        imagen=request.form["imagen"]
        stock=request.form["stock"]
        producto={"nombre": nombre, "categoria": categoria, "descripcion": descripcion, "precio": precio, "imagen": imagen, "stock": stock, "crear":True}
        ok=cargar_producto(producto)
        if not ok:
            flash("Error al guardar producto", "error")
        else:
            flash("Producto agregado con éxito", "success")
        return render_template('admin/modificar.html', producto={}, modificar= False )
    return render_template('admin/modificar.html', producto={}, modificar= False )
