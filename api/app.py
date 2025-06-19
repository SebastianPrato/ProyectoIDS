from flask import Flask
from flask_cors import CORS
from public.routes import public_bp
from admin.routes import admin_bp

app = Flask(__name__)
app.secret_key = 'clave-super-secreta'

CORS(app, supports_credentials=True, origins=["http://localhost:5000"])

app.register_blueprint(public_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/api/admin')

if __name__ == '__main__':
    app.run(port=5001)
