import mysql.connector
from flask import Flask, request, jsonify, abort, session, redirect
from flask_login import LoginManager
FRONT_BASE = "http://localhost:5001"
app = Flask(__name__)
app.secret_key = 'clave-super-secreta' 
app.config['SESSION_COOKIE_DOMAIN'] = '127.0.0.1'  # Configura para localhost
app.config['SESSION_COOKIE_SECURE'] = False        # Solo si no estás usando HTTPS

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
    data = request.form.to_dict()  # Captura datos del formulario en formato diccionario
    campos_requeridos = ['nombre', 'apellido', 'correo', 'contrasenia', 'recontrasenia']
    if not all(campo in data for campo in campos_requeridos): #Verifica que estén los datos
        return jsonify({"message": "Faltan datos obligatorios"}), 400
    
    if data['contrasenia'] != data['reconstrasenia']:
        return jsonify({"message": "Las contraseñas no coinciden"}), 400
    query_insert = """
        INSERT INTO usuarios (nombre, apellido, correo, contrasni)
        VALUES (%s, %s, %s)
    """
    query_check = "SELECT * FROM usuarios WHERE correo = %s"

    try:
        coneccion = get_db()
        cursor = coneccion.cursor()
        cursor.execute(query_check, (data['correo'],))
        if cursor.fetchone(): #Verifica que el correo no esté registrado
            return jsonify({"message": "El correo ya está registrado"}), 400
        values = (data['nombre'], data['apellido'], data['correo'], False)
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
        correo = request.form['correo']
        contrasenia = request.form['contrasenia']
        query = "SELECT * FROM usuarios WHERE correo = %s"
        connection = get_db()
        with connection.cursor() as cursor:
            cursor.execute(query, (correo,))
            usuario = cursor.fetchone()
            if usuario and usuario['contrasenia']==contrasenia: ## Verificar si el usuario existe y la contraseña es correcta
                session['usuario'] = usuario['id']
                session['nombre'] = usuario['nombre']
                if usuario['administrador']:
                    return redirect(f"{FRONT_BASE}/admin")  # Redirige a /admin
                return redirect(f"{FRONT_BASE}/")  # Redirigir a /
            else:
                return jsonify({'auth': False, "message": "Credenciales incorrectas"}), 401
    except Exception as e:
        return jsonify({'auth': False, 'message': f'Error al iniciar sesión: {str(e)}'}), 500
    finally:
        connection.close()

@app.route('/usuarios/logout', methods=['POST'])
def logout():
    session.clear()  # Limpiar todas las variables de sesión
    return redirect(f"{FRONT_BASE}/login")

@app.route('/productos/categoria/<int:categoria_id>', methods=['GET'])
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
@app.route('/usuario/admin/modificar_producto', methods=['POST'])
def modificar_producto():
    coneccion = get_db()
    cursor = coneccion.cursor(dictionary=True)
    data = request.json()
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

"""
    
"""


@app.route('/checkout', methods=['POST'])
def pagar():
    data = request.get_json() or {}
    cliente_id = data.get('cliente_id')
    items = data.get('items')
    if not cliente_id or not isinstance(items, list) or not items:
        abort(400, 'cliente_id e items son requeridos')

    db = get_db(); cur = db.cursor()
    try:

        # aca verificamos el  cliente
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



if __name__ == '__main__':
    app.run(port=5001)
