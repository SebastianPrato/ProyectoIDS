from flask import render_template, redirect, url_for, flash, session, request, Blueprint
from utils.forms import CategoriasForm
import requests

API_BASE = "http://127.0.0.1:5001/api"

admin_pedidos_bp = Blueprint('admin_pedidos', __name__)

#funciones

def obtener_pedidos():
    response=requests.get(f"{API_BASE}/admin/pedidos", cookies=request.cookies)
    if response.status_code==200:
        return response.json()

#rutas
@admin_pedidos_bp.route('/pedidos', methods=['GET'])
def pedidos():
    if session.get('administrador') != 1:
        return redirect(url_for('home'))
    
    pedidos = obtener_pedidos()

    lista_pedidos = []
    lista_totales = []
    
    i = 0
    while i < len(pedidos):
        subtotal = 0
        compra = []
        id_actual = pedidos[i]["id_compra"]
        
        while i < len(pedidos) and pedidos[i]["id_compra"] == id_actual:
            compra.append(pedidos[i])
            subtotal += float(pedidos[i]["precio"])*int(pedidos[i]["cantidad"])

            i += 1

        lista_totales.append(subtotal)
        lista_pedidos.append(compra)

    return render_template('admin/pedidos.html', pedidos=lista_pedidos, totales=lista_totales)