from flask import Flask, render_template, redirect, url_for, flash, session, request
from utils.forms import LoginForm, RegisterForm
from flask_cors import CORS
import requests

app = Flask(__name__)
app.secret_key = 'clave-super-secreta'  # Misma clave que en el backend
CORS(app)


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

def eliminar_categoria(id):
    response = requests.get(f"{API_BASE}/admin/usuario/admin/eliminar_categoria/{id}")
    if response.status_code == 200:
        return response.json()
    return response.json()

def listar_categorias():
    response = requests.get(f"{API_BASE}/admin/usuario/admin/listar_categorias")
    if response.status_code == 200:
        data = response.json()
        return data['categorias']
    return {}
def get_categoria(id):
    response = requests.get(f"{API_BASE}/admin/usuario/admin/categoria/{id}")
    if response.status_code == 200:
        data = response.json()
        return data
    return 

def obtener_compras_hechas():
    response=requests.get(f"{API_BASE}/miscompras")
    if response.status_code==200:
        return response.json()
    
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


@app.route('/', methods=['GET'])
def home():
    return render_template('public/home.html', categorias=listar_categorias(), productos=[], ingresos=[])


datoscompra = {
    "producto": "Teto Plush",
    "precio": 71,
    "cantidad": 2,
    "total": 142,
    "id": "#010408",
    "entrega": "Por despachar",
    "status": "Enviado / En tránsito"
    }


@app.route('/miscompras', methods=['GET'])
def miscompras():
    #Si no ha iniciado sesión, mostrar mensaje de que opcion hecha solo para personas que ya iniciaron sesión
    #Si no tiene compras, mostrar mensaje de "Aun no has realizado ninguna compra!"
    
    datoscompra = obtener_compras_hechas()
    return render_template('public/miscompras.html', compra=datoscompra)






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

"""@app.route('/miscompras', methods=['GET'])
def miscompras():
    return render_template('public/miscompras.html', seleccionados=obtener_productos_carrito())"""

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
        data = response.json()
        if response.status_code == 200:
            session['id'] = data['id']
            session['nombre'] = data['nombre']
            session['administrador'] = data['administrador']
            return redirect(url_for('home'))
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
    return redirect(url_for('home'))

# --------------------------------------------

@app.route('/pagar')
def pagar():
    return render_template('public/pago.html')

#--------------------ADMIN---------------------
@app.route('/admin/categorias', methods=['GET'])
def categorias():
    return render_template('admin/categorias.html', categorias=listar_categorias())

@app.route('/admin/categorias/eliminar/<id>', methods=['GET', 'POST'])
def eliminar_categorias(id):
    print(f"Método recibido: {request.method}")
    categoria = get_categoria(id)
    nombre_categoria = categoria[1]
    categoria_id = categoria[0]

    if request.method == 'POST':
        print("entre")
        response = requests.delete(f"{API_BASE}/admin/usuario/admin/eliminar_categoria/{id}")
        if response.status_code == 200:
            return redirect(url_for('categorias'))

    return render_template('admin/confirmacion.html',
                           nombre_categoria=nombre_categoria,
                           categoria_id=categoria_id)



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

    return render_template('admin/gestion.html')



if __name__ == '__main__':
    app.run(port=5000, debug=True)
