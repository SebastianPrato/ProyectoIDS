from flask import Flask, request, jsonify, abort, session, redirect
from db import get_connection

from flask_login import LoginManager
FRONT_BASE = "http://127.0.0.1:5000"
app = Flask(__name__)
app.secret_key = 'clave-super-secreta' 
app.config['SESSION_COOKIE_DOMAIN'] = '127.0.0.1'  # Configura para localhost
app.config['SESSION_COOKIE_SECURE'] = False        # Solo si no estás usando HTTPS

public_up = Blueprint('public', __name__)


@app.route('/miscompras', methods=['GET'])
def mostrar_mis_compras():
    if 'user_id' not in session:
        return jsonify({'error': 'No has iniciado sesión'}), 401

    user_id = session['user_id']

    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            compras.id_compra,
            compras.fecha,
            compras.entregado,
            productos.id_producto,
            productos.nombre AS nombre_producto,
            productos.precio,
            detalle_compras.cantidad
        FROM compras
        JOIN detalle_compras ON compras.id_compra = detalle_compras.compra_id
        JOIN productos ON productos.id_producto = detalle_compras.producto_id
        WHERE compras.cliente_id = %s;
    """, (user_id,))

    compras = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(compras)
    