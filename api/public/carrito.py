from flask import Blueprint, abort, jsonify, request, session
from db import get_connection

FRONT_BASE = "http://127.0.0.1:5000"

carrito_bp=Blueprint('carrito', __name__)

@carrito_bp.route('/', methods=['GET'])
def api_get_carrito():
    cliente_id = request.args.get('cliente_id', type=int)
    if not cliente_id:
        abort(400, 'Falta el cliente_id en query string')
    db = get_connection(); cur = db.cursor(dictionary=True)
    cur.execute("""
      SELECT c.id AS carrito_id,
             c.producto_id,
             p.nombre       AS nombre_producto,
             p.stock        AS stock_disponible,
             c.cantidad     AS cantidad_en_carrito
      FROM carrito c
      JOIN productos p ON c.producto_id = p.id
      WHERE c.cliente_id = %s
    """, (cliente_id,))
    return jsonify({"cliente_id": cliente_id, "items": cur.fetchall()}), 200

# agrego o actualizo item del carro.
@carrito_bp.route('/', methods=['POST'])
def api_post_carrito():
    data = request.get_json() or {}
    try:
        cid = int(data['cliente_id'])
        pid = int(data['producto_id'])
        qty = int(data['cantidad'])
    except Exception:
        abort(400, 'Se requieren cliente_id, producto_id y cantidad (enteros)')
    if qty <= 0: 
        abort(400, 'cantidad debe ser > 0')
    
    db = get_connection(); cur = db.cursor()

    cur.execute("SELECT 1 FROM clientes WHERE id=%s", (cid,))
    if not cur.fetchone():
        abort(404, 'cliente_id inválido')
    cur.execute("SELECT stock FROM productos WHERE id=%s", (pid,))
    row = cur.fetchone()
    if not row:
        abort(404, 'producto_id inválido')
    if qty > row[0]:
        abort(400, 'stock insuficiente')

    cur.execute(
      "SELECT id, cantidad FROM carrito WHERE cliente_id=%s AND producto_id=%s",
      (cid, pid)
    )
    existing = cur.fetchone()
    if existing:
      new_qty = existing[1] + qty
      cur.execute("UPDATE carrito SET cantidad=%s, fecha_agregado=NOW() WHERE id=%s",
                  (new_qty, existing[0]))
    else:
      cur.execute(
          "INSERT INTO carrito(cliente_id, producto_id, cantidad) VALUES(%s,%s,%s)",
                  (cid, pid, qty)
                  )
    db.commit()
    return jsonify({"msg":"Ítem agregado/actualizado"}), 201