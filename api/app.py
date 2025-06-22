import mysql.connector
import requests
from flask import Flask, request, jsonify, abort, session, redirect
from flask_login import LoginManager
from flask_cors import CORS
FRONT_BASE = "http://127.0.0.1:5001"
app = Flask(__name__)
app.secret_key = 'clave-super-secreta' 
app.config['SESSION_COOKIE_DOMAIN'] = '127.0.0.1'  # Configura para localhost
app.config['SESSION_COOKIE_SECURE'] = False        # Solo si no estás usando HTTPS
CORS(app)
def get_db():
    return mysql.connector.connect(
        host="localhost", user="admin", password="password", database="ludoteca",
        autocommit=False  # manejamos transacciones manualmente
    )

@app.route('/', methods=['GET'])
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


@app.route('/productos', methods=['GET'])
def productos():
    coneccion = get_db(); cursor = coneccion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    productos= cursor.fetchall()
    cursor.close()
    coneccion.close()
    return jsonify(productos), 200


@app.route('/productos/<int:producto_id>', methods=['GET'])
def producto_detalle(producto_id):
    coneccion = get_db(); cursor = coneccion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id=%s", (producto_id,))
    prod = cursor.fetchone()
    cursor.close()
    coneccion.close()
    if not prod: 
        abort(404, 'Producto no encontrado')
    return jsonify(prod), 200

@app.route('/registro', methods=['POST'])
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

@app.route('/usuario/login', methods=['POST'])
def login():
    try:
        user=request.get_json()
        query = "SELECT * FROM usuarios WHERE mail = %s"
        connection = get_db()
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(query, (user['email'],))
            usuario = cursor.fetchone()
            if usuario and usuario['contrasenia']==user['contrasenia']: ## Verificar si el usuario existe y la contraseña es correcta
                session['usuario'] = usuario['id']
                session['nombre'] = usuario['nombre']
                if usuario['administrador']:
                    return redirect(f"{FRONT_BASE}/admin")  # Redirige a /admin
                return redirect(f"{FRONT_BASE}/")  # Redirigir a /
            else:
                return jsonify({'auth': False, "message": "Credenciales incorrectas"}), 401
    except Exception as e:
        print(e)
        return jsonify({'auth': False, 'message': f'Error al iniciar sesión: {str(e)}'}), 500
    finally:
        connection.close()

@app.route('/usuarios/logout', methods=['POST'])
def logout():
    session.clear()  # Limpiar todas las variables de sesión
    return redirect(f"{FRONT_BASE}/login")

@app.route('/productos/categoria/<int:categoria_id>', methods=['POST'])
def api_categoria(categoria_id):
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM productos WHERE categoria=%s", (categoria_id,))
    productos=cur.fetchall()
    if not productos:
        abort(404, 'Producto no encontrado')
    return jsonify(productos), 200
# este endpoint trae todos los pedidos desde la tabla compras
@app.route('/usuario/admin/pedidos', methods=['GET'])
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
@app.route('/usuario/admin/pedidos/<int:id>', methods=['GET'])
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


if __name__ == '__main__':
    app.run(port=5001)
