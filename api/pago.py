@app.route('/api/confirmar_pago', methods=['POST'])
def confirmar_pago():
    data = request.get_json()

    numero = data.get('numero')
    nombre = data.get('nombre')
    vencimiento = data.get('vencimiento')
    cvv = data.get('cvv')

    if not (numero and nombre and vencimiento and cvv):
        return jsonify({'error': 'Faltan datos de la tarjeta'}), 400

    if not validar_tarjeta(numero):
        return jsonify({'error': 'Número de tarjeta inválido'}), 400

    user_id = data.get('user_id') #cambiar por metodo con el cual se matenga la sesion del usuario
    db = get_db()
    cursor = db.cursor()

    # Obtener productos del carrito
    cursor.execute("SELECT producto_id, cantidad FROM carrito WHERE usuario_id = %s", (user_id,))
    productos = cursor.fetchall()

    if not productos:
        return jsonify({'error': 'El carrito está vacío'}), 400

    # Registrar la compra
    cursor.execute("INSERT INTO compras (usuario_id, fecha) VALUES (%s, NOW())", (user_id,))
    compra_id = cursor.lastrowid

    # Insertar productos comprados
    for prod in productos:
        producto_id, cantidad = prod
        cursor.execute("""
            INSERT INTO compra_detalle (compra_id, producto_id, cantidad)
            VALUES (%s, %s, %s)
        """, (compra_id, producto_id, cantidad))

    # Vaciar carrito
    cursor.execute("DELETE FROM carrito WHERE usuario_id = %s", (user_id,))
    db.commit()

    return jsonify({'mensaje': 'Compra realizada con éxito', 'compra_id': compra_id})