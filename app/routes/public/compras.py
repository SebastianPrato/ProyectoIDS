from flask import render_template, Blueprint
import requests

API_BASE = "http://localhost:5001/api"

public_compras_bp = Blueprint('public_compras', __name__)

# Funciones
def obtener_productos_carrito():
    response=requests.get(f"{API_BASE}/carrito")
    if response.status_code==200:
        return response.json()
    return {}

def obtener_compras_hechas():
    response=requests.get(f"{API_BASE}/miscompras")
    if response.status_code==200:
        return response.json()


# Rutas
@public_compras_bp.route('/compras', methods=['GET'])
def compras():
    datoscompra = obtener_compras_hechas()
    return render_template('public/miscompras.html', compra=datoscompra)

@public_compras_bp.route('/carrito', methods=['GET'])
def carrito():
    return render_template('public/carrito.html', seleccionados=obtener_productos_carrito())

"""@app.route('/miscompras', methods=['GET'])
def miscompras():
    return render_template('public/miscompras.html', seleccionados=obtener_productos_carrito())"""

@public_compras_bp.route('/carrito/checkout')
def checkout():
    return render_template('public/checkout.html')

@public_compras_bp.route('/pagar')
def pagar():
    return render_template('public/pago.html')
