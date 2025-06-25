import mysql
from db import get_connection
from flask import request, jsonify, abort, Blueprint

FRONT_BASE = "http://localhost:5000"

public_bp = Blueprint('public', __name__)

@public_bp.route('/', methods=['GET'])
def inicio():
    coneccion=get_connection()
    cursor= coneccion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos ORDER BY id_producto DESC LIMIT 8")
    recientes=cursor.fetchall()
    cursor.execute("SELECT * FROM productos LIMIT 8")
    destacados=cursor.fetchall()
    cursor.close()
    coneccion.close()
    return jsonify({'recientes':recientes, 'destacados':destacados}), 200
<<<<<<< HEAD


=======
>>>>>>> 8cb23cc28efd2f7edf68400c18115d9cdefbafe4
