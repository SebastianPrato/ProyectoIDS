import mysql.connector
from flask import Flask, request, jsonify, abort, session, redirect

from flask_login import LoginManager
FRONT_BASE = "http://127.0.0.1:5000"
app = Flask(__name__)
app.secret_key = 'clave-super-secreta' 
app.config['SESSION_COOKIE_DOMAIN'] = '127.0.0.1'  # Configura para localhost
app.config['SESSION_COOKIE_SECURE'] = False        # Solo si no estás usando HTTPS

public_bp = Blueprint('public', __name__)

def get_db():
    return mysql.connector.connect(
        host="localhost", user="mauro", password="1234", database="ludoteca",
        autocommit=False  # manejamos transacciones manualmente
    )

@app.route('/miscompras', methods=['GET'])
def mostrar_mis_compras():
    coneccion=get_db()
    cursor= coneccion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos ORDER BY  id DESC LIMIT 8")