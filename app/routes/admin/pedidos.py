from flask import render_template, redirect, url_for, flash, session, request, Blueprint
from utils.forms import CategoriasForm
import requests

API_BASE = "http://127.0.0.1:5001/api"

admin_pedidos_bp = Blueprint('admin_pedidos', __name__)

#funciones


#rutas
@admin_pedidos_bp.route('/pedidos', methods=['GET'])
def categorias():
    if session.get('administrador') != 1:
        return redirect(url_for('home'))
    return render_template('admin/pedidos.html')