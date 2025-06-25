from flask import Blueprint, abort, jsonify
from db import get_connection

FRONT_BASE = "http://127.0.0.1:5000"

productos_bp=Blueprint('productos', __name__)

@productos_bp.route('/', methods=['GET'])
def productos():
    coneccion = get_connection()
    cursor = coneccion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    productos= cursor.fetchall()
    cursor.close()
    coneccion.close()
    return jsonify(productos), 200

@productos_bp.route('/<int:producto_id>', methods=['GET'])
def producto_detalle(producto_id):
    coneccion = get_connection() 
    cursor = coneccion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id_producto=%s", (producto_id,))
    producto = cursor.fetchone()
    cursor.close()
    coneccion.close()
    if not producto: 
        abort(404, 'Producto no encontrado')
    return jsonify(producto), 200

@productos_bp.route('/categoria/<int:categoria_id>', methods=['GET'])
def api_categoria(categoria_id):
    coneccion = get_connection()
    cursor = coneccion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE categoria=%s", (categoria_id,))
    productos=cursor.fetchall()
    if not productos:
        abort(404, 'Categoria no encontrado')
    return jsonify(productos), 200