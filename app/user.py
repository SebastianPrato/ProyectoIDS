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
        return redirect(url_for("modificar", id_producto=id_producto)) #esto recien lo modifique, no se si funciona pero la idea es que si no funca te traiga los datos 
        #datos de nuevo o algo asi
    return render_template('modificar.html', producto=juego, modificar= True )

@app.route('/admin/cargar', methods=['GET', 'POST']) #cumple pero tienen que adaptar la tabla producto de la db sin rating
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
            return redirect(url_for('home_admin'))
        return redirect(url_for('modificar', id_producto=int(id)))
    return render_template('gestion.html')
