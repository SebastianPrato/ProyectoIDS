from flask import render_template, redirect, url_for, session, Blueprint, request
import requests

from routes.public.productos import listar_categorias

API_BASE = "http://localhost:5001/api"

public_bp = Blueprint('public', __name__)

# Funciones
def obtener_inicio():
    response=requests.get(f"{API_BASE}/", cookies=request.cookies)
    if response.status_code==200:
        return response.json()
    return {}


# Rutas
@public_bp.route('/', methods=['GET'])
def home():
    if session.get('administrador') == 1:
        return redirect(url_for('admin.home_admin'))
    categorias = listar_categorias()
    productos = obtener_inicio()
    return render_template('public/home.html', categorias=categorias, productos=productos, ingresos=[])

@public_bp.route('/about_us', methods=['GET'])
def about_us():
    return render_template('public/about_us.html')

@public_bp.route('/FAQs', methods=['GET'])
def faqs():
    return render_template('public/faqs.html')
