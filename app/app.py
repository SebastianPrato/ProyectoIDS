from flask import Flask, render_template, request, redirect, url_for, flash
from productos_data import juegos #diccionario de ejemplo, luego cambiar por extraccion de la base datos

import requests

app = Flask(__name__)
app.secret_key = 'cualquier_clave_para_flash'  # agrego el flash para cualquier mensaje para procesar "POSTs"

API_BASE = "http://localhost:5001"

def obtener_productos():
    print("obteniendo productos")
    response = requests.get(f"{API_BASE}/api/productos")
    if response.status_code == 200:
        return response.json()
    return {}

def obtener_categoria(categoria):
    response=requests.get(f"{API_BASE}/api/productos/categorrias/{categoria}")
    if response.status_code==200:
        return response.json()
    return {}

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html', categorias=[], productos=[], ingresos=[])

@app.route('/miscompras')
def miscompras():
    return render_template('miscompras.html')

@app.route('/productos', methods=['GET'])
def productos():
    return render_template('productos.html', juegos=obtener_productos())

@app.route('/productos/<int:producto_id>', methods=['GET'])
def producto_detalle(producto_id):
   return render_template('detalle.html')




@app.route('/carrito', methods=['GET'])
def carrito():
    return render_template('carrito.html')


@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        # ponemos un formulario de contacto aca?
        flash('Mensaje enviado, ¡gracias!')
        return redirect(url_for('contacto'))
    return render_template('contact.html')


@app.route('/carrito/checkout')
def checkout():
    return render_template('checkout.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # aca agarramos el form['nombre'], form['mail'], etc
        flash('Registro recibido, revisa tu email.')
        return redirect(url_for('home'))
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # comparamos las credenciales con la API /api/login si quieren
        flash('Login exitoso.')
        return redirect(url_for('home'))
    return render_template('login.html')



"""
@app.route('/productos/categorias', methods=['GET'])
def categorias():
    return render_template('categorias.html')
"""    
@app.route('/productos/categorias/<categoria>', methods=['GET'])
def categoria_detalle(categoria):
    return render_template('categoria_detalle.html', categoria=obtener_categoria(categoria))


@app.route('/about_us', methods=['GET'])
def about_us():
    return render_template('about_us.html')

@app.route('/faq', methods=['GET'])
def faq():
    return render_template('faq.html')

#@app.route('/productos/<int:producto_id>', methods=['GET'])
#def producto_detalle(producto_id):
#    producto = next((j for j in juegos if j["id"] == producto_id), None)
#    if producto:
#        return render_template('producto_detalle.html', producto=producto)
#    else:
#        return "Producto no encontrado", 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)



