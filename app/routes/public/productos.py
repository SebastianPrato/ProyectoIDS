from flask import render_template, Blueprint, request, session, redirect, url_for
import requests

from routes.public.compras import modificar_carrito

API_BASE = "http://127.0.0.1:5001/api"

public_productos_bp = Blueprint('public_productos', __name__)

# Funciones
def obtener_productos():
    response = requests.get(f"{API_BASE}/productos")
    if response.status_code == 200:
        return response.json()
    return {}

def obtener_producto(id):
    response = requests.get(f"{API_BASE}/productos/{id}")
    if response.status_code == 200:
        return response.json()
    return {}

def listar_categorias():
    response = requests.get(f"{API_BASE}/categorias")
    if response.status_code == 200:
        data = response.json()
        return data['categorias']
    return {}

def obtener_productos_categoria(id_categoria):
    response=requests.get(f"{API_BASE}/productos/categoria/{id_categoria}")
    if response.status_code==200:
        return response.json()
    return {}


# Rutas
@public_productos_bp.route('/', methods=['GET'])
def productos():
    categorias = listar_categorias()
    return render_template('public/productos.html', productos = obtener_productos(), categorias=categorias)

@public_productos_bp.route('/<int:id_producto>', methods=['GET', 'POST'])
def producto_detalle(id_producto):
    producto=obtener_producto(id_producto)
    categorias = listar_categorias()

    message = None

    if request.method == "POST":
        if not session.get('id_cliente'):
            message = "Debe iniciar sesión para agregar productos al carrito"
        else:
            message = modificar_carrito(request.form).get('message')
    
    return render_template('public/detalle.html', producto = producto, categorias=categorias, message=message)

@public_productos_bp.route('/categoria/<int:id_categoria>', methods=['GET'])
def productos_categoria(id_categoria):
    categorias = listar_categorias()
    return render_template('public/productos.html', productos = obtener_productos_categoria(id_categoria), categorias=categorias, categoria_activa=id_categoria)
