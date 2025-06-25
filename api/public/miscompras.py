from flask import Blueprint, jsonify, session
from db import get_connection

FRONT_BASE = "http://127.0.0.1:5000"

miscompras_bp=Blueprint('miscompras', __name__)

@miscompras_bp.route('/', methods=['GET'])
def mostrar_mis_compras():
    # if 'user_id' not in session:
    #     return jsonify({'error': 'No has iniciado sesión'}), 401
    # user_id = session['user_id']

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
        WHERE compras.cliente_id = 1;
    """ #, (user_id,)
    )

    compras = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(compras), 200