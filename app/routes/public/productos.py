from flask import render_template, Blueprint
import requests

API_BASE = "http://localhost:5001/api"

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
        print(data['categorias'])
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

@public_productos_bp.route('/<int:id_producto>', methods=['GET'])
def producto_detalle(id_producto):
   producto=obtener_producto(id_producto)
   return render_template('public/detalle.html', producto = producto)

@public_productos_bp.route('/categoria/<int:id_categoria>', methods=['GET'])
def productos_categoria(id_categoria):
    categorias = listar_categorias()
    return render_template('public/productos.html', productos = obtener_productos_categoria(id_categoria), categorias=categorias, categoria_activa=id_categoria)
