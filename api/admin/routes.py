import mysql.connector
from flask import Blueprint, request, jsonify, abort

admin_bp = Blueprint('admin', __name__)

def get_db():
    return mysql.connector.connect(
        host="localhost", user="root", password="", database="flask_app", use_pure=True,
        autocommit=False  # manejamos transacciones manualmente
    )