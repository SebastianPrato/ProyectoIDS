from flask import jsonify, render_template, Blueprint, request, session, redirect, url_for
import requests

API_BASE = "http://127.0.0.1:5001/api"

public_compras_bp = Blueprint('public_compras', __name__)

# Funciones
def modificar_carrito(producto):
    response = requests.post(f"{API_BASE}/compras/carrito", json=producto, cookies=request.cookies)
    if response.status_code == 201 or response.status_code == 400 or response.status_code == 404:
        return response.json()
    return {}

def pagar_carrito(form):
    response = requests.post(f"{API_BASE}/compras/pagar", json=form, cookies=request.cookies)
    if response.status_code == 201 or response.status_code == 400:
        return response.json()
    return {}

def obtener_compras_hechas():
    response=requests.get(f"{API_BASE}/compras", cookies=request.cookies)
    if response.status_code==200:
        return response.json()


# Rutas
@public_compras_bp.route('/carrito', methods=['GET', 'POST'])
def carrito():
    if not session.get('id_cliente'):
        return redirect(url_for('public.home'))
    
    productos = {}
    message = None
    total = 0

    if request.method == "POST":
        message = modificar_carrito(request.form).get('message')

    response=requests.get(f"{API_BASE}/compras/carrito", cookies=request.cookies)
    if response.status_code == 200:
        productos = response.json()
    elif response.status_code == 400:
        message = response.json().get('message')

    for producto in productos:
        total += float(producto['precio']) * producto['cantidad']

    return render_template('public/carrito.html', productos=productos, message=message, total=total)

@public_compras_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if not session.get('id_cliente'):
        return redirect(url_for('public.home'))
    productos = {}
    message = ""
    total = 0

    if request.method == "POST":
        message = pagar_carrito(request.form).get('message')

    response=requests.get(f"{API_BASE}/compras/carrito", cookies=request.cookies)
    if response.status_code == 200:
        productos = response.json()
    elif response.status_code == 400:
        message = response.json().get('message')

    for producto in productos:
        total += float(producto['precio']) * producto['cantidad']

    return render_template('public/checkout.html', productos=productos, message=message, total=total)

@public_compras_bp.route('/compras', methods=['GET'])
def compras():
    if not session.get('id_cliente'):
        return redirect(url_for('public.home'))
    datos_compras = obtener_compras_hechas()

    lista_compras = []
    lista_totales = []
    
    i = 0
    while i < len(datos_compras):
        subtotal = 0
        compra = []
        id_actual = datos_compras[i]["id_compra"]
        
        while i < len(datos_compras) and datos_compras[i]["id_compra"] == id_actual:
            compra.append(datos_compras[i])
            subtotal += float(datos_compras[i]["precio"])*int(datos_compras[i]["cantidad"])

            i += 1

        lista_totales.append(subtotal)
        lista_compras.append(compra)

    #lista_compras = [compra1, compra2, compra3...]
    #compra1 = [{'cantidad': 1, 'estado': 1, 'fecha': 'Thu, 26 Jun 2025 01:18:45 GMT',...{}}
    
    return render_template('public/miscompras.html', compras=lista_compras, totales=lista_totales)
