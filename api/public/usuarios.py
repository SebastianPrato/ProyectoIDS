from flask import Blueprint, request, jsonify, redirect
from db import get_connection

FRONT_BASE = "http://127.0.0.1:5000"

usuarios_bp=Blueprint('usuarios', __name__)

@usuarios_bp.route('/registro', methods=['POST'])
def registro():
    data=request.get_json()
    query_insert = """
        INSERT INTO usuarios (nombre, apellido, mail, contrasenia)
        VALUES (%s, %s, %s, %s)
    """
    query_check = "SELECT * FROM usuarios WHERE mail = %s"

    coneccion = None
    cursor = None

    try:
        coneccion = get_connection()
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

@usuarios_bp.route('/login', methods=['POST'])
def login():

    connection = None

    try:
        user=request.get_json()
        query = "SELECT * FROM usuarios WHERE mail = %s"
        connection = get_connection()
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(query, (user['email'],))
            usuario = cursor.fetchone()
            if (usuario and (usuario['contrasenia']==user['contrasenia'])): ## Verificar si el usuario existe y la contraseña es correcta
                return jsonify({'auth': True, 'id':usuario['id_usuario'], 'nombre':usuario['nombre']}), 200
            else:
                return jsonify({'auth': False, "message": "Credenciales incorrectas"}), 401
    except Exception as e:
        print(e)
        return jsonify({'auth': False, 'message': f'Error al iniciar sesión: {str(e)}'}), 500
    finally:
        connection.close()