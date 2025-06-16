from flask import Flask
from public.routes import public_bp
from admin.routes import admin_bp

app = Flask(__name__)
app.register_blueprint(public_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/api/admin')


if __name__ == '__main__':
    app.run(port=5001)
