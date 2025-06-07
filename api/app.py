import mysql.connector
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="localhost", user="root", password="", database="flask_app",
        autocommit=False  # manejamos transacciones manualmente
    )



@app.route('/api/productos', methods=['GET'])
def api_productos():
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT id, nombre, stock,image_url FROM productos")
    return jsonify(cur.fetchall()), 200


@app.route('/api/productos/<int:producto_id>', methods=['GET'])
def api_producto_detalle(producto_id):
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT id, nombre, stock,descripcion,image_url FROM productos WHERE id=%s", (producto_id,))

    prod = cur.fetchone()
    if not prod: abort(404, 'Producto no encontrado')
    return jsonify(prod), 200

@app.route('/api/registro', methods=['POST'])
def api_registro():

    data = request.get_json() or {}
    for k in ('nombre','apellido','mail','contraseña'):
        if not data.get(k):
            abort(400, f'Falta {k}')
    db = get_db(); cur =  db.cursor()
    try:
        cur.execute(
            "INSERT INTO clientes(nombre,apellido,mail,contraseña) VALUES(%s,%s,%s,%s)",
            (data['nombre'],data['apellido'],data['mail'],data['contraseña'])
        )
        db.commit()
        return jsonify({'cliente_id': cur.lastrowid}), 201
    except mysql.connector.Error as e:

        db.rollback()
        abort(400, str(e))

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json() or {}
    mail, pwd = data.get('mail'), data.get
    ('contraseña')
    if not mail or not pwd: abort(400, 'Mail y contraseña requeridos')
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT id, nombre FROM clientes WHERE mail=%s AND contraseña=%s",
        (mail, pwd)
    )
    user = cur.fetchone()

    if not user: abort(401, 'Credenciales inválidas')
    return jsonify(user), 200





@app.route('/api/carrito', methods=['GET'])

def api_carrito():
    # Simulación temporal
    return jsonify([]), 200

@app.route('/api/compra', methods=['POST'])
def api_compra():
    data = request.get_json() or {}
    cliente_id = data.get('cliente_id')
    items = data.get('items')
    if not cliente_id or not isinstance(items, list) or not items:
        abort(400, 'cliente_id e items son requeridos')

    db = get_db(); cur = db.cursor()
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

@app.route('/api/productos/<int:producto_id>', methods=['PATCH'])

def api_update_stock(producto_id):
    data = request.get_json() or {}
    new_stock = data.get('stock')
    if new_stock is None:
        abort(400, 'stock requerido')
    db = get_db(); cur = db.cursor()
    try:
        cur.execute("UPDATE productos SET stock=%s WHERE id=%s", (new_stock, producto_id))
        db.commit()
        return jsonify({'msg':'Stock actualizado'}), 200
    except mysql.connector.Error as e:
        db.rollback()
        abort(400, str(e))

@app.route('/api/compras', methods=['GET'])
def api_compras():
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("""
                
      SELECT c.id, c.cliente_id, c.fecha, c.entregado,
             GROUP_CONCAT(CONCAT(dc.producto_id,':',dc.cantidad)) AS items
      FROM compras c
      JOIN detalle_compras dc ON c.id=dc.compra_id
      GROUP BY c.id
    """)

    return jsonify(cur.fetchall()), 200




@app.route('/api/productos/categorias/<categoria>', methods=['GET'])
def api_categoria(categoria):
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT id,nombre,stock FROM productos WHERE categoria=%s", (categoria,))
    return jsonify(cur.fetchall()), 200

if __name__ == '__main__':
    app.run(port=5001)



@app.route('/api/carrito', methods=['GET'])
def api_get_carrito():
    cliente_id = request.args.get('cliente_id', type=int)
    if not cliente_id:
        abort(400, 'Falta cliente_id en query string')
    db = get_db(); cur = db.cursor(dictionary=True)
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
    items = cur.fetchall()
    return jsonify({"cliente_id": cliente_id, "items": items}), 200

# agrego o actualizo item del carro.
@app.route('/api/carrito', methods=['POST'])
def api_post_carrito():
    data = request.get_json() or {}
    try:
        cid = int(data['cliente_id'])
        pid = int(data['producto_id'])
        qty = int(data['cantidad'])
    except Exception:
        abort(400, 'Se requieren cliente_id, producto_id y cantidad (enteros)')
    if qty <= 0: abort(400, 'cantidad debe ser > 0')
    db = get_db(); cur = db.cursor()

    cur.execute("SELECT 1 FROM clientes WHERE id=%s", (cid,))
    if not cur.fetchone(): abort(404, 'cliente_id inválido')
    cur.execute("SELECT stock FROM productos WHERE id=%s", (pid,))
    row = cur.fetchone()
    if not row: abort(404, 'producto_id inválido')
    if qty > row[0]: abort(400, 'stock insuficiente')

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
      cur.execute("INSERT INTO carrito(cliente_id, producto_id, cantidad) VALUES(%s,%s,%s)",
                  (cid, pid, qty))
    db.commit()
    return jsonify({"msg":"Ítem agregado/actualizado"}), 201


