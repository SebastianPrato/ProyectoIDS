from flask import Flask, render_template, redirect, url_for, session
from flask_cors import CORS
from utils.forms import LoginForm
import requests

from routes.public.public import public_bp
from routes.public.productos import public_productos_bp
from routes.public.usuarios import public_usuarios_bp
from routes.public.compras import public_compras_bp

from routes.admin.admin import admin_bp
from routes.admin.productos import admin_productos_bp
from routes.admin.categorias import admin_categorias_bp
from routes.admin.pedidos import admin_pedidos_bp

API_BASE = "http://127.0.0.1:5001/api"

app = Flask(__name__)
app.secret_key = 'clave-super-secreta'  # Misma clave que en el backend
CORS(app)


# Blueprints public
app.register_blueprint(public_bp)
app.register_blueprint(public_productos_bp, url_prefix='/productos')
app.register_blueprint(public_usuarios_bp, url_prefix='')
app.register_blueprint(public_compras_bp, url_prefix='')

#Bluprints admin
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(admin_productos_bp, url_prefix='/admin')
app.register_blueprint(admin_categorias_bp, url_prefix='/admin')
app.register_blueprint(admin_pedidos_bp, url_prefix='/pedidos')


# Rutas comunes
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit(): 
        email = form.email.data
        password = form.password.data
        usuario={"email":email, "contrasenia":password}
        response = requests.post(f"{API_BASE}/usuarios/login", json=usuario)
        data = response.json()
        if response.status_code == 200:
            session['id_cliente'] = data['id']
            session['nombre_cliente'] = data['nombre']
            session['administrador'] = data['administrador']
            return redirect(url_for('public.home'))
        elif response.status_code == 401:
            error = data["message"]
            return render_template('login.html', form=form, error=error)
        elif response.status_code == 500:
            error = data["message"]
            return render_template('login.html', form=form, error=error)
    return render_template('login.html', form=form)
 
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('public.home'))

if __name__ == '__main__':
    app.run(port=5000, debug=True)


