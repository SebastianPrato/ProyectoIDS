CREATE TABLE IF NOT EXISTS productos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  categoria INT NOT NULL,
  nombre VARCHAR(100) NOT NULL,
  descripcion VARCHAR(250) NOT NULL,
  precio INT NOT NULL,
  imagen VARCHAR(250) NOT NULL,
  stock INT NOT NULL
  precio DECIMAL(10, 2) NOT NULL,
  image_url VARCHAR(255) NOT NULL,
);

CREATE TABLE IF NOT EXISTS clientes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  apellido VARCHAR(50) NOT NULL,
  mail VARCHAR(100) UNIQUE NOT NULL,
  contrasenia VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS administradores (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  apellido VARCHAR(50) NOT NULL,
  mail VARCHAR(100) UNIQUE NOT NULL,
  contrasenia VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS compras (
  id INT AUTO_INCREMENT PRIMARY KEY,
  cliente_id INT NOT NULL,
  fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
  entregado BOOLEAN DEFAULT FALSE,
  FOREIGN KEY(cliente_id) REFERENCES clientes(id)
);

CREATE TABLE IF NOT EXISTS detalle_compras (
  id INT AUTO_INCREMENT PRIMARY KEY,
  compra_id INT NOT NULL,
  producto_id INT NOT NULL,
  cantidad INT NOT NULL,
  FOREIGN KEY(compra_id) REFERENCES compras(id),
  FOREIGN KEY(producto_id) REFERENCES productos(id)
);
