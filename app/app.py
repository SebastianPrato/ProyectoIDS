from flask import Flask, render_template, request, redirect, url_for, flash, session
from productos_data import juegos, categorias #diccionario de ejemplo, luego cambiar por extraccion de la base datos

app = Flask(__name__)
app.secret_key = 'clave-super-secreta'  # Misma clave que en el backend
app.config['SESSION_COOKIE_DOMAIN'] = '127.0.0.1'
app.config['SESSION_COOKIE_SECURE'] = False  # agrego el flash para cualquier mensaje para procesar "POSTs"

API_BASE = "http://localhost:5000"

def obtener_productos():
    response = request.get(f"{API_BASE}/productos")
    if response.status_code == 200:
        return response.json()
    return {}

def obtener_producto(id):
    response = request.get(f"{API_BASE}/productos{id}")
    if response.status_code == 200:
        return response.json()
    return {}

def obtener_categoria(categoria):
    response=request.get(f"{API_BASE}/productos/categoria/{categoria}")
    if response.status_code==200:
        return response.json()
    return {}

def obtener_inicio():
    response=request.get(f"{API_BASE}/")
    if response.status_code==200:
        return response.json()
    return {}
def obtener_productos_carrito():
    response=request.get(f"{API_BASE}/carrito")
    if response.status_code==200:
        return response.json()
    return {}

@app.route('/', methods=['GET'])
def home():
    productos=obtener_inicio()
    return render_template('home.html', categorias=[], destacados=productos['destacados'], ingresos=productos['recientes'] )

@app.route('/productos', methods=['GET'])
def productos():
    return render_template('productos.html', juegos=obtener_productos(), categorias=[])

@app.route('/productos/<int:producto_id>', methods=['GET'])
def producto_detalle(producto_id):
   producto=obtener_producto(producto_id)
   return render_template('detalle.html', producto=obtener_producto(producto_id))

@app.route('/about_us', methods=['GET'])
def about_us():
    return render_template('about_us.html')

@app.route('/productos/categorias/<categoria>', methods=['GET'])
def categoria_detalle(categoria):
    return render_template('productos.html', juegos=obtener_categoria(categoria), categorias=categorias)

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')
 
@app.route('/carrito', methods=['GET'])
def carrito():
    return render_template('carrito.html', seleccionados=obtener_productos_carrito())


@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    return render_template('contact.html')


@app.route('/carrito/checkout')
def checkout():
    return render_template('checkout.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    return render_template('registro.html')


if __name__ == '__main__':
    app.run(port=5000, debug=True)



