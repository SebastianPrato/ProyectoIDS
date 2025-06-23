import mysql.connector
from flask import Blueprint, request, jsonify, session

admin_bp = Blueprint('admin', __name__)

def get_db():
    return mysql.connector.connect(
        host="localhost", user="root", password="", database="ludoteca", use_pure=True,
        autocommit=False  # manejamos transacciones manualmente
    )

@admin_bp.route('/usuario/admin/pedidos', methods=['GET'])
def ver_pedidos():
    if 'usuario' not in session: #ESTA ES LA MANERA DE PREGUNTAR SI SE INICIÓ SESIÓN
        print("Usuario no autenticado.")
        return jsonify({"auth": False, "message": "Usuario no autenticado"}), 401
    query = "SELECT * FROM compras;"
    try:
        coneccion = get_db()
        with coneccion.cursor() as cursor:
            cursor.execute(query)
            resultado = cursor.fetchall()
            pedidos = []
            for row in resultado:
                pedido = {
                    'id': row['id'],
                    'cliente': row['cliente_id'],
                    'estado': row['estado'],
                    'fecha': row['fecha'],
                    'estado': row['entregado']
                }
                pedidos.append(pedido)

            return jsonify(pedidos), 200
    except Exception as e:
        print(f"Error en ver_pedidos: {e}")
        return jsonify({'message': f'Error al obtener pedidos: {str(e)}'}), 500
    finally:
        coneccion.close()


#este endpoint es para ver un pedido es especifico
@admin_bp.route('/usuario/admin/pedidos/<int:id>', methods=['GET'])
def ver_pedido(id):
    if 'usuario' not in session: #Se comprueba que esté la sesion iniciada
        print("Usuario no autenticado.")
        return jsonify({"auth": False, "message": "Usuario no autenticado"}), 401
    query = "SELECT * FROM detalle_compras WHERE compra_id=%s;"
    try:
        coneccion = get_db()
        with coneccion.cursor() as cursor:
            cursor.execute(query, (id,))
            resultado = cursor.fetchall()
            productos=[]
            for row in resultado:
                pedido = {
                    'compra': resultado['compra_id'],
                    'producto': resultado['producto_id'],
                    'cantidad': resultado['estado'],
                }
                productos.append(pedido)
            return jsonify(productos), 200
    except Exception as e:
        print(f"Error en ver_pedido: {e}")
        return jsonify({'message': f'Error al obtener pedido: {str(e)}'}), 500
    finally:
        coneccion.close()


# este endpoint esta diseñado para que cuando se reciba la id desde el front,
# modifique los datos del producto, sin tocar la id, si la id no viene en la request
# entonces es un producto nuevo 
@admin_bp.route('/usuario/admin/modificar_producto', methods=['POST'])
def modificar_producto():
    coneccion = get_db()
    cursor = coneccion.cursor(dictionary=True)
    data = request.get_json()
    id = int(data.get("categoria"))
    categoria = int(data.get("categoria"))
    nombre=data.get("nombre")
    precio = float(data.get("precio"))
    stock=int(data.get("stock"))
    descripcion=data.get("descripcion")
    imagen=data.get("imagen")
    cursor.execute("SELECT id, nombre, stock,descripcion,image_url FROM productos WHERE id=%s;", (id,))
    producto = cursor.fetchone()
    if producto:
        cursor.execute("UPDATE productos SET categoria = %s, nombre= %s, precio= %s, stock=%s, descripcion= %s, imagen=%s WHERE id = %s;", 
                       (categoria, nombre, precio, stock, descripcion, imagen, id,))
    else:
        cursor.execute("INSERT INTO nombre_de_la_tabla (categoria, nombre, descripcion, precio, imagen, stock) VALUES (%s, %s, %s, %s, %s, %s);",
                        (categoria, nombre, descripcion, precio, imagen, stock,))
    coneccion.commit()
    cursor.close()
    coneccion.close()
    return ("Producto modificado/agregado", 201)

@admin_bp.route('/usuario/admin/crear_categoria', methods=['POST'])
def crear_categoria():
    coneccion = get_db()
    cursor = coneccion.cursor()
    data = request.get_json()
    nombre = data.get("nombre")
    cursor.execute("INSERT INTO categoria (nombre) VALUES (%s);",
                  (nombre,))
    coneccion.commit()
    cursor.close()
    coneccion.close()
    return jsonify({"message":"Categoria agregada"}), 201

@admin_bp.route('/usuario/admin/editar_categoria/<int:categoria_id>', methods=['PUT'])
def editar_categoria(categoria_id):
    coneccion = get_db()
    cursor = coneccion.cursor()
    data = request.get_json()
    nuevo_nombre = data.get("nombre")
    cursor.execute("SELECT id, nombre FROM categoria WHERE id=%s",
                  (categoria_id,))
    categoria = cursor.fetchone()
    if categoria:
        cursor.execute("UPDATE categoria SET nombre=%s WHERE id=%s",
                       (nuevo_nombre, categoria_id,))
        coneccion.commit()
        cursor.close()
        coneccion.close()
        return jsonify({"message":"Categoria editada"}), 200
    cursor.close()
    coneccion.close()
    return jsonify({"message":"Categoria no encontrada"}), 404

@admin_bp.route('/usuario/admin/eliminar_categoria/<int:categoria_id>', methods=['DELETE'])
def eliminar_categoria(categoria_id):
    coneccion = get_db()
    cursor = coneccion.cursor()
    cursor.execute("SELECT id, nombre FROM categoria WHERE id=%s",
                  (categoria_id,))
    categoria = cursor.fetchone()
    if categoria:
        cursor.execute("DELETE FROM categoria WHERE id=%s",
                       (categoria_id,))
        coneccion.commit()
        cursor.close()
        coneccion.close()
        return jsonify({"message":"Categoria eliminada"}), 200
    cursor.close()
    coneccion.close()
    return jsonify({"message":"Categoria no encontrada"}), 404

@admin_bp.route('usuario/admin/listar_categorias', methods=['GET'])
def listar_categorias():
    coneccion = get_db()
    cursor = coneccion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categoria")
    categorias = cursor.fetchall()
    cursor.close()
    coneccion.close()
    return jsonify({"categorias": categorias}), 200


##############################################################################################

@public_bp.route('/productos/<int:producto_id>', methods=['PATCH'])
def api_update_stock(producto_id):
    data = request.get_json() or {}
    new_stock = data.get('stock')
    if new_stock is None:
        abort(400, 'stock requerido')
    db = get_connection(); cur = db.cursor()
    try:
        cur.execute("UPDATE productos SET stock=%s WHERE id=%s", (new_stock, producto_id))
        db.commit()
        return jsonify({'msg':'Stock actualizado'}), 200
    except mysql.connector.Error as e:
        db.rollback()
        abort(400, str(e))



@app.route('/usuario/admin/modificar/<int:id>', methods=['GET', 'POST'])
def modificar_producto(id):
    coneccion = get_db()
    cursor = coneccion.cursor(dictionary=True)
    data = request.get_json()
    print(data)
    cursor.execute("SELECT * FROM productos WHERE id=%s;", (id,))
    producto = cursor.fetchone()
    if producto:
        cursor.execute("UPDATE productos SET categoria = %s, nombre= %s, precio= %s, stock=%s, descripcion= %s, imagen=%s WHERE id = %s;", 
                       (int(data["categoria"]), data["nombre"], float(data["precio"]), int(data["stock"]), data["descripcion"], data["imagen"], id,))
    coneccion.commit()
    cursor.close()
    coneccion.close()
    return jsonify({"message": "Producto modificado exitosamente"}), 201

@app.route('/usuario/admin/cargar', methods=['GET', 'POST'])
def cargar():
    coneccion = get_db()
    cursor = coneccion.cursor(dictionary=True)
    data = request.get_json()
    cursor.execute("INSERT INTO productos (categoria, nombre, descripcion, precio, imagen, stock) VALUES (%s, %s, %s, %s, %s, %s);", 
                       (int(data["categoria"]), data["nombre"], data["descripcion"], float(data["precio"]), data["imagen"],int(data["stock"]),))
    coneccion.commit()
    cursor.close()
    coneccion.close()
    return jsonify({"message": "Producto agregado exitosamente"}), 201


@app.route('/usuario/admin/borrar/<int:id>', methods=['DELETE'])
def borrar(id):
    coneccion = get_db()
    cursor = coneccion.cursor(dictionary=True)
    cursor.execute("DELETE FROM productos WHERE id = %s;", (id,))
    if cursor.rowcount == 0:
                return jsonify({"message": "Producto no encontrado"}), 404
    coneccion.commit()
    cursor.close()
    coneccion.close()
    return jsonify({"message": "Producto eliminado exitosamente"}), 200
