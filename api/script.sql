CREATE TABLE IF NOT EXISTS categorias (
  id_categoria INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS productos (
  id_producto INT AUTO_INCREMENT PRIMARY KEY,
  id_categoria INT NOT NULL,
  nombre VARCHAR(100) NOT NULL,
  descripcion VARCHAR(250) NOT NULL,
  imagen VARCHAR(250) NOT NULL,
  stock INT NOT NULL,
  precio DECIMAL(10,2) NOT NULL,
  FOREIGN KEY(id_categoria) REFERENCES categorias(id_categoria)
);

CREATE TABLE IF NOT EXISTS usuarios (
  id_usuario INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  apellido VARCHAR(50) NOT NULL,
  mail VARCHAR(100) UNIQUE NOT NULL,
  contrasenia VARCHAR(255) NOT NULL,
  administrador BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS compras (
  id_compra INT AUTO_INCREMENT PRIMARY KEY,
  id_cliente INT NOT NULL,
  fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
  estado BOOLEAN DEFAULT FALSE,
  FOREIGN KEY(id_cliente) REFERENCES usuarios(id_usuario)
);

CREATE TABLE IF NOT EXISTS detalle_compras (
  id_detalle_compra INT AUTO_INCREMENT PRIMARY KEY,
  id_compra INT NOT NULL,
  id_producto INT NOT NULL,
  cantidad INT NOT NULL,
  FOREIGN KEY(id_compra) REFERENCES compras(id_compra),
  FOREIGN KEY(id_producto) REFERENCES productos(id_producto)
);
