from flask import Blueprint, jsonify
from db import get_connection

categorias_bp = Blueprint('public_categorias', __name__)


@categorias_bp.route('/', methods=['GET'])
def listar_categorias():
    coneccion = get_connection()
    cursor = coneccion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categorias")
    categorias = cursor.fetchall()
    cursor.close()
    coneccion.close()
    return jsonify({"categorias": categorias}), 200
