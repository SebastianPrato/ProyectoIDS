from flask import Flask, render_template, request, redirect, url_for, flash, session
from utils.forms import LoginForm, RegisterForm
from flask_cors import CORS
import requests
import sys
app = Flask(__name__)
app.secret_key = 'clave-super-secreta'
app.config['SESSION_COOKIE_DOMAIN'] = '127.0.0.1'
app.config['SESSION_COOKIE_SECURE'] = False
CORS(app)

API_BASE = "http://127.0.0.1:5000"

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
    response=requests.get(f"{API_BASE}/")
    if response.status_code==200:
        return response.json()
    return {}
def gestionar_stock(producto, id):
    response=requests.post(f"{API_BASE}/usuario/admin/modificar/{id}", json=producto)
    if response.status_code==201:
        return True
    return False

def cargar_producto(producto):
    response=requests.post(f"{API_BASE}/usuario/admin/cargar", json=producto)
    if response.status_code==201:
        return True
    return False


def obtener_productos_carrito():
    response=requests.get(f"{API_BASE}/carrito")
    if response.status_code==200:
        return response.json()
    return {}

@app.route('/', methods=['GET'])
def home():
    productos=obtener_inicio()
    return render_template('home.html', categorias=categorias, destacados=productos['destacados'], ingresos=productos['recientes'] )

@app.route('/productos', methods=['GET'])
def productos():
    return render_template('productos.html', juegos=obtener_productos(), categorias=categorias)

@app.route('/productos/<int:producto_id>', methods=['GET'])
def producto_detalle(producto_id):
   producto=obtener_producto(producto_id)
   return render_template('detalle.html', producto=obtener_producto(producto_id))

@app.route('/about_us', methods=['GET'])
def about_us():
    return render_template('about_us.html')


@app.route('/FAQs', methods=['GET'])
def faqs():
    return render_template('faqs.html')


@app.route('/productos/categorias/<categoria>', methods=['GET'])
def categoria_detalle(categoria):
    return render_template('productos.html', juegos=obtener_categoria(categoria), categorias=categorias)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit(): 
        email = form.email.data
        password = form.password.data
        usuario={"email":email, "contrasenia":password}
        response = requests.post(f"{API_BASE}/usuario/login", json=usuario)
        if response.status_code == 200:
            return redirect(url_for('home')) 
    return render_template('login.html', form=form)
 
@app.route('/carrito', methods=['GET'])
def carrito():
    return render_template('carrito.html', seleccionados=obtener_productos_carrito())


@app.route('/carrito/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegisterForm()

    if form.validate_on_submit():
        nombre = form.name.data.strip()
        apellido = form.surname.data.strip()
        email = form.email.data
        contrasenia = form.password.data.strip()
        usuario={"nombre": nombre, "apellido": apellido, "email":email, "contrasenia":contrasenia}
        response = requests.post(f"{API_BASE}/registro", json=usuario)
        if response.status_code == 200:
            return redirect(url_for('login')) 
        else:
            flash("Hubo un error al registrar. Intenta nuevamente.") 
    return render_template('registro.html', form=form)
@app.route('/admin/modificar/<int:id_producto>', methods=['GET', 'POST']) #cumple lo basico
def modificar(id_producto):
    juego=obtener_producto(id_producto)
    if request.method== "POST":
        nombre=request.form["nombre"]
        categoria=request.form["categoria"]
        descripcion=request.form["descripcion"]
        precio=request.form["precio"]
        imagen=request.form["imagen"]
        stock=request.form["stock"]
        producto_m={"nombre": nombre, "categoria": categoria, "descripcion": descripcion, "precio": precio, "imagen": imagen, "stock": stock, "crear":False}
        ok=gestionar_stock(producto_m, id=id_producto)
        if not ok:
            flash("Error al guardar producto", "error")
        else:
            flash("Producto agregado con éxito", "success")
        return redirect(url_for("modificar", id_producto=juego['id'])) 
    return render_template('modificar.html', producto=juego, modificar= True )

@app.route('/admin/cargar', methods=['GET', 'POST']) 
def cargar():
    if request.method== "POST":
        nombre=request.form["nombre"]
        categoria=request.form["categoria"]
        descripcion=request.form["descripcion"]
        precio=request.form["precio"]
        imagen=request.form["imagen"]
        stock=request.form["stock"]
        producto={"nombre": nombre, "categoria": categoria, "descripcion": descripcion, "precio": precio, "imagen": imagen, "stock": stock, "crear":True}
        ok=cargar_producto(producto)
        if not ok:
            flash("Error al guardar producto", "error")
        else:
            flash("Producto agregado con éxito", "success")
        return redirect(url_for("cargar", modificar=False))
    return render_template('modificar.html', producto={}, modificar= False )
@app.route('/admin', methods=['GET', 'POST'])
def home_admin():
    if request.method == "POST":
        id = request.form["producto"]
        if not id:
            flash("Debes ingresar un ID", "warning")
            return redirect(url_for('home_admin'))

        try:
            id_int = int(id)
        except ValueError:
            flash("ID inválido", "warning")
            return redirect(url_for('home_admin'))

        producto = obtener_producto(id_int)
        if not producto:
            flash("No se encontró ningún producto con ese ID", "warning")
            return redirect(url_for('home_admin'))

        return redirect(url_for('modificar', id_producto=id_int))

    return render_template('gestion.html')


if __name__ == '__main__':
    app.run(port=5001, debug=True)



