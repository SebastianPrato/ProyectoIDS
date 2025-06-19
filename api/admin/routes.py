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
