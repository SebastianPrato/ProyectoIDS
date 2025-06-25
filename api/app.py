from flask import Flask
from flask_cors import CORS

from public.routes import public_bp
from public.productos import productos_bp
from public.categorias import categorias_bp
from public.usuarios import usuarios_bp
from public.compras import compras_bp

from admin.admin import admin_bp

app = Flask(__name__)
app.secret_key = 'clave-super-secreta'

CORS(app, supports_credentials=True, origins=["http://localhost:5000"])

app.register_blueprint(public_bp, url_prefix='/api')
app.register_blueprint(productos_bp, url_prefix='/api/productos')   
app.register_blueprint(categorias_bp, url_prefix='/api/categorias')
app.register_blueprint(usuarios_bp, url_prefix='/api/usuarios')
app.register_blueprint(compras_bp, url_prefix='/api/compras')

app.register_blueprint(admin_bp, url_prefix='/api/admin')

if __name__ == '__main__':
    app.run(port=5001)
