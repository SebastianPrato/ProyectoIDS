from flask import Blueprint, request, jsonify, abort
import mysql
from db import get_connection

FRONT_BASE = "http://127.0.0.1:5000"

compra_bp=Blueprint('compra', __name__)



@compra_bp.route('/compras', methods=['GET'])
def api_compras():
    coneccion = get_connection()
    cursor = coneccion.cursor(dictionary=True)
    cursor.execute("""
      SELECT c.id, c.cliente_id, c.fecha, c.entregado,
             GROUP_CONCAT(CONCAT(dc.producto_id,':',dc.cantidad)) AS items
      FROM compras c
      JOIN detalle_compras dc ON c.id=dc.compra_id
      GROUP BY c.id
    """)
    resultado = cursor.fetchall()
    return jsonify(resultado), 200


@compra_bp.route('/compra', methods=['POST'])
def api_compra():
    data = request.get_json() or {}
    cliente_id = data.get('cliente_id')
    items = data.get('items')
    if not cliente_id or not isinstance(items, list) or not items:
        abort(400, 'cliente_id e items son requeridos')

    db = get_connection(); cur = db.cursor()
    try:

        # aca verificamos el  cliente
        cur.execute("SELECT 1 FROM clientes WHERE id=%s", (cliente_id,))
        if not cur.fetchone():
            abort(400, 'cliente_id no válido')

        # ponemos la compra
        cur.execute("INSERT INTO compras(cliente_id) VALUES(%s)", (cliente_id,))
        compra_id = cur.lastrowid

        # ponemos el detalle y verificamos el  producto
        for it in items:
            pid, qty = it.get('producto_id'), it.get('cantidad')
            cur.execute("SELECT 1 FROM productos WHERE id=%s", (pid,))
            if not cur.fetchone():
                abort(400, f'producto_id {pid} no existe')
            cur.execute(
                "INSERT INTO detalle_compras(compra_id, producto_id, cantidad) "
                "VALUES(%s,%s,%s)", (compra_id, pid, qty)
            )
        db.commit()
        return jsonify({'compra_id': compra_id}), 201

    except mysql.connector.Error as e:
        db.rollback()
        abort(400, str(e))
