CREATE TABLE IF NOT EXISTS productos (
  id_producto INT AUTO_INCREMENT PRIMARY KEY,
  precio INT NOT NULL;
  categoria INT NOT NULL,
  nombre VARCHAR(100) NOT NULL,
  descripcion VARCHAR(250) NOT NULL,
  imagen VARCHAR(250) NOT NULL,
  stock INT NOT NULL
);

CREATE TABLE IF NOT EXISTS usuarios (
  id_usuario INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  apellido VARCHAR(50) NOT NULL,
  mail VARCHAR(100) UNIQUE NOT NULL,
  contrasenia VARCHAR(255) NOT NULL,
  administrador BOOLEAN DEFAULT FALSE,
);

CREATE TABLE IF NOT EXISTS compras (
  id_compra INT AUTO_INCREMENT PRIMARY KEY,
  cliente_id INT NOT NULL,
  fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
  entregado BOOLEAN DEFAULT FALSE,
  pagado BOOLEAN DEFAULT FALSE,
  FOREIGN KEY(cliente_id) REFERENCES clientes(id)
);

CREATE TABLE IF NOT EXISTS detalle_compras (
  compra_id INT NOT NULL,
  producto_id INT NOT NULL,
  cantidad INT NOT NULL,2
  FOREIGN KEY(compra_id) REFERENCES compras(id_compra),
  FOREIGN KEY(producto_id) REFERENCES productos(id_producto)
);
