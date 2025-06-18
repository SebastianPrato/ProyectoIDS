from flask import Flask, render_template, redirect, url_for, flash, session, request
from utils.forms import LoginForm, RegisterForm
import requests

app = Flask(__name__)
app.secret_key = 'clave-super-secreta'  # Misma clave que en el backend

API_BASE = "http://localhost:5001/api"

categorias=["Estrategia", "Azar", "Rol", "Cartas", "Habilidad", "Cooperativos", "Solitario", "Adultos"]

def obtener_productos():
    response = requests.get(f"{API_BASE}/productos")
    if response.status_code == 200:
        return response.json()
    return {}

def obtener_producto(id):
    response = requests.get(f"{API_BASE}/productos/{id}")
    if response.status_code == 200:
        return response.json()
    return {}

def obtener_categoria(categoria):
    response=requests.get(f"{API_BASE}/productos/categoria/{categoria}")
    if response.status_code==200:
        return response.json()
    return {}

def obtener_inicio():
    response=requests.get(f"{API_BASE}/", cookies=request.cookies)
    if response.status_code==200:
        return response.json()
    return {}

def obtener_productos_carrito():
    response=requests.get(f"{API_BASE}/carrito")
    if response.status_code==200:
        return response.json()
    return {}

@app.route('/', methods=['GET'])
def home():
    productos=obtener_inicio()
    return render_template('public/home.html', categorias=[], destacados=productos['destacados'], ingresos=productos['recientes'] )

@app.route('/productos', methods=['GET'])
def productos():
    return render_template('public/productos.html', juegos=obtener_productos(), categorias=[])

@app.route('/productos/<int:producto_id>', methods=['GET'])
def producto_detalle(producto_id):
   producto=obtener_producto(producto_id)
   return render_template('public/detalle.html', producto=obtener_producto(producto_id))

@app.route('/about_us', methods=['GET'])
def about_us():
    return render_template('public/about_us.html')


@app.route('/FAQs', methods=['GET'])
def faqs():
    return render_template('public/faqs.html')

@app.route('/productos/categorias/<categoria>', methods=['GET'])
def categoria_detalle(categoria):
    return render_template('public/productos.html', juegos=obtener_categoria(categoria), categorias=categorias)

@app.route('/carrito', methods=['GET'])
def carrito():
    return render_template('public/carrito.html', seleccionados=obtener_productos_carrito())

@app.route('/miscompras', methods=['GET'])
def miscompras():
    return render_template('public/miscompras.html', seleccionados=obtener_productos_carrito())

@app.route('/carrito/checkout')
def checkout():
    return render_template('public/checkout.html')

# ------------------ USUARIOS ------------------

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegisterForm()

    if form.validate_on_submit():
        nombre = form.name.data.strip()
        apellido = form.surname.data.strip()
        email = form.email.data
        contrasenia = form.password.data.strip()
        usuario={"nombre": nombre, "apellido": apellido, "email":email, "contrasenia":contrasenia}
        response = requests.post(f"{API_BASE}/usuarios/registro", json=usuario)
        if response.status_code == 200:
            return redirect(url_for('login'))  # O tu ruta de login
        else:
            flash("Hubo un error al registrar. Intenta nuevamente.") 
    return render_template('public/registro.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit(): 
        email = form.email.data
        password = form.password.data
        usuario={"email":email, "contrasenia":password}
        response = requests.post(f"{API_BASE}/usuarios/login", json=usuario)
        if response.status_code == 200:
            data = response.json()
            session['id'] = data['id']
            session['nombre'] = data['nombre']
            return redirect(url_for('home'))
    return render_template('login.html', form=form)
 
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# --------------------------------------------

@app.route('/pagar')
def pagar():
    return render_template('public/pago.html')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
