import mysql.connector
from flask import Blueprint, request, jsonify, session

from db import get_connection

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/pedidos', methods=['GET'])
def mostrar_pedidos():
    if 'id_cliente' not in session:
        return jsonify({'error': 'No has iniciado sesión'}), 401

    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            compras.id_cliente,
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
        WHERE compras.estado = 1;""")
    compras = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(compras), 200



@admin_bp.route('/pedidos/<int:id>', methods=['GET'])
def ver_pedido(id):
    if 'usuario' not in session: #Se comprueba que esté la sesion iniciada
        print("Usuario no autenticado.")
        return jsonify({"auth": False, "message": "Usuario no autenticado"}), 401
    query = "SELECT * FROM detalle_compras WHERE compra_id=%s;"
    try:
        coneccion = get_connection()
        with coneccion.cursor() as cursor:
            cursor.execute(query, (id,))
            resultado = cursor.fetchall()
            productos=[]
            for row in resultado:
                pedido = {
                    'compra': resultado['compra_id'],
                    'producto': resultado['producto_id'],
                    'cantidad': resultado['cantidad'],
                }
                productos.append(pedido)
            return jsonify(productos), 200
    except Exception as e:
        print(f"Error en ver_pedido: {e}")
        return jsonify({'message': f'Error al obtener pedido: {str(e)}'}), 500
    finally:
        coneccion.close()

@admin_bp.route('/crear_categoria', methods=['POST'])
def crear_categoria():
    coneccion = get_connection()
    cursor = coneccion.cursor()
    data = request.get_json()
    nombre = data.get("nombre")
    cursor.execute("INSERT INTO categorias (nombre) VALUES (%s);",
                  (nombre,))
    coneccion.commit()
    cursor.close()
    coneccion.close()
    return jsonify({"message":"Categoria agregada"}), 201

@admin_bp.route('/editar_categoria/<int:categoria_id>', methods=['PUT'])
def editar_categoria(categoria_id):
    coneccion = get_connection()
    cursor = coneccion.cursor()
    data = request.get_json()
    nuevo_nombre = data.get("nombre")
    cursor.execute("SELECT id_categoria, nombre FROM categorias WHERE id_categoria=%s",
                  (categoria_id,))
    categoria = cursor.fetchone()
    if categoria:
        cursor.execute("UPDATE categorias SET nombre=%s WHERE id_categoria=%s",
                       (nuevo_nombre, categoria_id,))
        coneccion.commit()
        cursor.close()
        coneccion.close()
        return jsonify({"message":"Categoria editada"}), 200
    cursor.close()
    coneccion.close()
    return jsonify({"message":"Categoria no encontrada"}), 404

@admin_bp.route('/eliminar_categoria/<int:categoria_id>', methods=['DELETE'])
def eliminar_categoria(categoria_id):
    coneccion = get_connection()
    cursor = coneccion.cursor()
    cursor.execute("SELECT id_categoria, nombre FROM categorias WHERE id_categoria=%s",
                  (categoria_id,))
    categoria = cursor.fetchone()
    if categoria:
        cursor.execute("DELETE FROM categorias WHERE id_categoria=%s",
                       (categoria_id,))
        coneccion.commit()
        cursor.close()
        coneccion.close()
        return jsonify({"message":"Categoria eliminada"}), 200
    cursor.close()
    coneccion.close()
    return jsonify({"message":"Categoria no encontrada"}), 404

@admin_bp.route('/categorias', methods=['GET'])
def listar_categorias():
    coneccion = get_connection()
    cursor = coneccion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categorias")
    categorias = cursor.fetchall()
    cursor.close()
    coneccion.close()
    return jsonify({"categorias": categorias}), 200

@admin_bp.route('/categorias/<int:categoria_id>', methods=['GET'])
def get_categoria(categoria_id):
    coneccion = get_connection()
    cursor = coneccion.cursor()
    cursor.execute("SELECT id_categoria, nombre "
                    "FROM categorias WHERE id_categoria=%s",
                  (categoria_id,))
    categoria = cursor.fetchone()
    if categoria:
        cursor.close()
        coneccion.close()
        return jsonify(categoria), 200
    cursor.close()
    coneccion.close()
    return jsonify({"message":"Categoria no encontrada"}), 404

@admin_bp.route('/modificar/<int:id>', methods=['GET', 'POST'])
def modificar_producto(id):
    coneccion = get_connection()
    cursor = coneccion.cursor(dictionary=True)
    data = request.get_json()
    print(data)
    cursor.execute("SELECT * FROM productos WHERE id_producto=%s;", (id,))
    producto = cursor.fetchone()
    if producto:
        cursor.execute("UPDATE productos SET id_categoria = %s, nombre= %s, precio= %s, stock=%s, descripcion= %s, imagen=%s WHERE id_producto = %s;", 
                       (int(data["id_categoria"]), data["nombre"], float(data["precio"]), int(data["stock"]), data["descripcion"], data["imagen"], id,))
        coneccion.commit()
    cursor.close()
    coneccion.close()
    if not producto: 
        return jsonify({"message":"Producto no encontrado"}), 404
    return jsonify({"message": "Producto modificado exitosamente"}), 201

@admin_bp.route('/cargar', methods=['GET', 'POST'])
def cargar():
    coneccion = get_connection()
    cursor = coneccion.cursor(dictionary=True)
    data = request.get_json()
    cursor.execute("INSERT INTO productos (id_categoria, nombre, descripcion, precio, imagen, stock) VALUES (%s, %s, %s, %s, %s, %s);", 
                       (int(data["id_categoria"]), data["nombre"], data["descripcion"], float(data["precio"]), data["imagen"],int(data["stock"]),))
    coneccion.commit()
    cursor.close()
    coneccion.close()
    return jsonify({"message": "Producto agregado exitosamente"}), 201


@admin_bp.route('/borrar/<int:id>', methods=['DELETE'])
def borrar(id):
    coneccion = get_connection()
    cursor = coneccion.cursor(dictionary=True)
    cursor.execute("DELETE FROM productos WHERE id_producto = %s;", (id,))
    if cursor.rowcount == 0:
        cursor.close()
        coneccion.close()
        return jsonify({"message": "Producto no encontrado"}), 404
    coneccion.commit()
    cursor.close()
    coneccion.close()
    return jsonify({"message": "Producto eliminado exitosamente"}), 200
