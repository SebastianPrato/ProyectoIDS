@app.route('/usuario/admin/modificar/<int:id>', methods=['GET', 'POST'])
def modificar_producto(id):
    coneccion = get_db()
    cursor = coneccion.cursor(dictionary=True)
    data = request.get_json()
    print(data)
    cursor.execute("SELECT * FROM productos WHERE id=%s;", (id,))
    producto = cursor.fetchone()
    if producto:
        cursor.execute("UPDATE productos SET categoria = %s, nombre= %s, precio= %s, stock=%s, descripcion= %s, imagen=%s WHERE id = %s;", 
                       (int(data["categoria"]), data["nombre"], int(data["precio"]), int(data["stock"]), data["descripcion"], data["imagen"], id,))
    coneccion.commit()
    cursor.close()
    coneccion.close()
    return jsonify({"message": "Producto modificado exitosamente"}), 201

@app.route('/usuario/admin/cargar', methods=['GET', 'POST'])
def cargar():
    coneccion = get_db()
    cursor = coneccion.cursor(dictionary=True)
    data = request.get_json()
    cursor.execute("INSERT INTO productos (categoria, nombre, descripcion, precio, imagen, stock) VALUES (%s, %s, %s, %s, %s, %s);", 
                       (int(data["categoria"]), data["nombre"], int(data["precio"]), int(data["stock"]), data["descripcion"], data["imagen"],))
    coneccion.commit()
    cursor.close()
    coneccion.close()
    return jsonify({"message": "Producto agregado exitosamente"}), 201

@app.route('/usuario/admin/borrar/<int:id>', methods=['DELETE'])
def borrar(id):
    coneccion = get_db()
    cursor = coneccion.cursor(dictionary=True)
    data = request.get_json()
    cursor.execute("DELETE FROM productos WHERE id = %s;", (id))
    if cursor.rowcount == 0:
                return jsonify({"message": "Producto no encontrado"}), 404
    coneccion.commit()
    cursor.close()
    coneccion.close()
    return jsonify({"message": "Producto eliminado exitosamente"}), 200
