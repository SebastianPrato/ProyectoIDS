from flask import Blueprint, request, jsonify, abort, session, redirect
from db import get_connection

FRONT_BASE = "http://127.0.0.1:5000"

compras_bp=Blueprint('compras', __name__)

@compras_bp.route('/', methods=['GET'])
def mostrar_mis_compras():
    if 'id_cliente' not in session:
        return jsonify({'error': 'No has iniciado sesión'}), 401
    user_id = session['id_cliente']

    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            compras.id_compra,
            compras.fecha,
            compras.estado,
            productos.id_producto,
            productos.nombre AS nombre_producto,
            productos.precio,
            detalle_compras.cantidad,
            productos.imagen
        FROM compras
        JOIN detalle_compras ON compras.id_compra = detalle_compras.id_compra
        JOIN productos ON productos.id_producto = detalle_compras.id_producto
        WHERE compras.id_cliente = %s;""" , (user_id,)
    )
    compras = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(compras), 200

@compras_bp.route('/carrito', methods=['POST'])
def modificar_carrito():
    data = request.get_json() or {}
    try:
        cid = session['id_cliente']
        pid = int(data['id_producto'])
        qty = int(data['cantidad'])
    except Exception as e:
        return jsonify({"message":'Se requiere estar autenticado, el id del producto y la cantidad (enteros)'}), 400
    if qty <= 0: 
        return jsonify({"message":'Cantidad debe ser mayor a 0'}), 400
  
    db = get_connection(); 
    cur = db.cursor()

    # Validación de usuario
    cur.execute("SELECT 1 FROM usuarios WHERE id_usuario = %s", (cid,))
    if not cur.fetchone():
        return jsonify({"message":'Id de cliente inválido'}), 404

    # Validación de stock producto
    cur.execute("SELECT stock FROM productos WHERE id_producto = %s", (pid,))
    row = cur.fetchone()
    if not row:
        return jsonify({"message":'Id de producto inválido'}), 404
    if qty > row[0]:
        return jsonify({"message":'Stock insuficiente'}), 400

    # Validacmos si ya existe un carrito
    cur.execute("SELECT id_compra FROM compras WHERE id_cliente = %s AND estado = 0", (cid,))
    carrito = cur.fetchone()
    detalle = None

    if carrito:
        # Validación si ya existe el producto en el carrito
        cur.execute("SELECT id_detalle_compra FROM detalle_compras WHERE id_compra = %s AND id_producto = %s", (carrito[0], pid))
        detalle = cur.fetchone()
        if detalle:
            cur.execute("UPDATE detalle_compras SET cantidad = %s WHERE id_detalle_compra = %s", (qty, detalle[0]))
        else:
            cur.execute("INSERT INTO detalle_compras(id_compra, id_producto, cantidad) VALUES(%s,%s,%s)",(carrito[0], pid, qty))
    
    #  Creamos carrito y su detalle
    else:
        cur.execute("INSERT INTO compras(id_cliente , fecha, estado) VALUES(%s, NOW(), 0)", (cid,))
        id_compra = cur.lastrowid
        cur.execute("INSERT INTO detalle_compras(id_compra, id_producto, cantidad) VALUES(%s,%s,%s)",(id_compra, pid, qty))
    db.commit()

    mensaje = None
    if detalle:
        mensaje = "Producto modificado exitosamente"
    else:
        mensaje = "Producto agregado exitosamente"

    return jsonify({"message":mensaje}), 201

@compras_bp.route('/carrito', methods=['GET'])
def obtener_carrito():
    try:
        cid = session['id_cliente']
    except Exception:
        return jsonify({"message":'Se requiere estar autenticado'}), 400
    db = get_connection(); 
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT d.id_detalle_compra, p.id_producto, p.nombre, p.precio, d.cantidad FROM detalle_compras d " \
                "INNER JOIN productos p ON d.id_producto = p.id_producto " \
                "WHERE id_compra = (SELECT id_compra FROM compras WHERE id_cliente = %s AND estado = 0)", (cid,))
    carrito = cur.fetchall()
    return jsonify(carrito), 200

@compras_bp.route('/carrito', methods=['DELETE'])
def borrar_producto_carrito():
    try:
        cid = session['id_cliente']
    except Exception:
        return jsonify({"message":'Se requiere estar autenticado'}), 400
    
    data = request.get_json() or {}
    id_detalle = int(data['id_detalle_compra'])
    db = get_connection(); 
    cur = db.cursor()
    cur.execute("DELETE FROM detalle_compras WHERE id_detalle_compra = %s", (id_detalle,))
    db.commit()
    return jsonify({"message":'Producto eliminado exitosamente'}), 200

def validar_tarjeta(numero: str) -> bool:
    numero = numero.replace(" ", "")
    if not numero.isdigit() or not 13 <= len(numero) <= 19:
        return False

    # Algoritmo de Luhn
    total = 0
    reverse_digits = numero[::-1]
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:
            n = n * 2
            if n > 9:
                n = n - 9
        total += n
    return total % 10 == 0

@compras_bp.route('/pagar', methods=['POST'])
def pagar_carrito():
    data = request.get_json()

    # Validación de datos
    numero = data.get('numero')
    nombre = data.get('nombre')
    vencimiento = data.get('vencimiento')
    cvv = data.get('cvv')

    if not (numero and nombre and vencimiento and cvv):
        return jsonify({'message': 'Faltan datos de la tarjeta'}), 400

    if not validar_tarjeta(numero):
        return jsonify({'message': 'Número de tarjeta inválido'}), 400

    id_cliente = session['id_cliente']
    db = get_connection()
    cursor = db.cursor()

    # Obtener productos del carrito
    cursor.execute("SELECT 1 FROM compras WHERE id_cliente = %s AND estado = 0", (id_cliente,))

    if not cursor.fetchone():
        return jsonify({'message': 'El carrito está vacío'}), 400

    # Comprar carrito - cambiar estado
    cursor.execute("UPDATE compras SET estado = 1 WHERE id_cliente = %s AND estado = 0", (id_cliente,))
    db.commit()

    return jsonify({'message': 'Compra realizada con éxito'}), 201
