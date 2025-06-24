import mysql.connector
from flask import Flask, request, jsonify, abort, redirect, Blueprint
import requests

from flask_login import LoginManager
FRONT_BASE = "http://localhost:5000"

public_bp = Blueprint('public', __name__)

def get_db():
    return mysql.connector.connect(
        host="localhost", user="mauro", password="1234", database="ludoteca", use_pure=True,
        autocommit=False  # manejamos transacciones manualmente
    )

@public_bp.route('/', methods=['GET'])
def inicio():
    coneccion=get_db()
    cursor= coneccion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos ORDER BY  id DESC LIMIT 8")
    recientes=cursor.fetchall()
    cursor.execute("SELECT * FROM productos LIMIT 8")
    destacados=cursor.fetchall()
    cursor.close()
    coneccion.close()
    return jsonify({'recientes':recientes, 'destacados':destacados}), 200

@public_bp.route('/productos', methods=['GET'])
def productos():
    coneccion = get_db()
    cursor = coneccion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    productos= cursor.fetchall()
    cursor.close()
    coneccion.close()
    return jsonify(productos), 200

@public_bp.route('/productos/<int:producto_id>', methods=['GET'])
def producto_detalle(producto_id):
    coneccion = get_db(); cursor = coneccion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id=%s", (producto_id,))
    prod = cursor.fetchone()
    cursor.close()
    coneccion.close()
    if not prod: 
        abort(404, 'Producto no encontrado')
    return jsonify(prod), 200

@public_bp.route('/usuarios/registro', methods=['POST'])
def registro():
    data=request.get_json()
    query_insert = """
        INSERT INTO usuarios (nombre, apellido, mail, contrasenia)
        VALUES (%s, %s, %s, %s)
    """
    query_check = "SELECT * FROM usuarios WHERE mail = %s"

    try:
        coneccion = get_db()
        cursor = coneccion.cursor()
        cursor.execute(query_check, (data['email'],))
        if cursor.fetchone(): #Verifica que el correo no esté registrado
            return jsonify({"message": "El correo ya está registrado"}), 400
        values = (data['nombre'], data['apellido'], data['email'], data['contrasenia'])
        cursor.execute(query_insert, values)
        coneccion.commit()
        return redirect(f"{FRONT_BASE}/login")
    except Exception as e:
        print(f"Error al registrar usuario: {e}")
        return jsonify({'message': f'Error al registrar usuario: {str(e)}'}), 500
    finally:
        if cursor:
            try:
                cursor.close()
            except Exception as e:
                print(f"Error al cerrar el cursor: {e}")
        if coneccion:
            try:
                coneccion.close()
            except Exception as e:
                print(f"Error al cerrar la conexión: {e}")

@public_bp.route('/usuarios/login', methods=['POST'])
def login():
    try:
        user=request.get_json()
        query = "SELECT * FROM usuarios WHERE mail = %s"
        connection = get_db()
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(query, (user['email'],))
            usuario = cursor.fetchone()
            if usuario and usuario['contrasenia']==user['contrasenia']: ## Verificar si el usuario existe y la contraseña es correcta
                return jsonify({'auth': True, 'id':usuario['id'], 'nombre':usuario['nombre'], 'administrador': usuario['administrador']}), 200
            else:
                return jsonify({'auth': False, "message": "Credenciales incorrectas"}), 401
    except Exception as e:
        print(e)
        return jsonify({'auth': False, 'message': f'Error al iniciar sesión: {str(e)}'}), 500
    finally:
        connection.close()

@public_bp.route('/productos/categoria/<int:categoria_id>', methods=['GET'])
def api_categoria(categoria_id):
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM productos WHERE categoria=%s", (categoria_id,))
    productos=cur.fetchall()
    if not productos:
        abort(404, 'Producto no encontrado')
    return jsonify(productos), 200

@public_bp.route('/compra', methods=['POST'])
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

@public_bp.route('/productos/<int:producto_id>', methods=['PATCH'])
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

@public_bp.route('/compras', methods=['GET'])
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

@public_bp.route('/carrito', methods=['GET'])
def api_get_carrito():
    cliente_id = request.args.get('cliente_id', type=int)
    if not cliente_id:
        abort(400, 'Falta el cliente_id en query string')
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
    return jsonify({"cliente_id": cliente_id, "items": cur.fetchall()}), 200

# agrego o actualizo item del carro.
@public_bp.route('/carrito', methods=['POST'])
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
    
    db = get_db(); cur = db.cursor()

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
