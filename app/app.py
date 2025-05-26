from flask import Flask, render_template, request, redirect, url_for

app:Flask = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/productos')
def productos():
    return render_template('productos.html')

@app.route('/productos/<int:producto_id>')
def producto_detalle(producto_id):
    # Aquí podrías obtener los detalles del producto de una base de datos
    return render_template('producto_detalle.html', producto_id=producto_id)

@app.route('/carrito')
def carrito():  
    # Aquí podrías obtener los productos del carrito de una base de datos o sesión
    return render_template('carrito.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    return render_template('registro.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/productos/categorias')
def categorias():
    return render_template('categorias.html')

@app.route('/productos/categorias/<categoria>')
def categoria_detalle(categoria):
    # Aquí podrías obtener los productos de la categoría de una base de datos
    return render_template('categoria_detalle.html', categoria=categoria)

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

