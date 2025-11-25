-- ===================================================
-- 🚀 CREACIÓN DE LA BASE DE DATOS
-- ===================================================
CREATE DATABASE IF NOT EXISTS inventario_cema;
USE inventario_cema;

-- ===================================================
-- 🧩 TABLA USUARIOS (CORREGIDA: se quitó rol)
-- ===================================================
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT(5) AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    nombre_completo TEXT
);

INSERT INTO usuarios (username, password, nombre_completo)
VALUES ('admin', '1234', 'Administrador General')
ON DUPLICATE KEY UPDATE username = username;

-- ===================================================
-- 🧩 TABLA CATEGORÍAS (CORREGIDA)
-- ===================================================
CREATE TABLE IF NOT EXISTS categorias (
    id_categoria INT(5) AUTO_INCREMENT PRIMARY KEY,
    nombre TEXT NOT NULL,
    descripcion TEXT
);

-- ===================================================
-- 🧩 TABLA PRODUCTOS (CORREGIDA)
-- ===================================================
CREATE TABLE IF NOT EXISTS productos (
    id_producto INT(5) AUTO_INCREMENT PRIMARY KEY,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    precio DECIMAL(6,2) NOT NULL,
    stock INT DEFAULT 0,
    id_categoria INT(5),
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
);

-- ===================================================
-- 🧩 TABLA PROVEEDORES (AGREGADA)
-- ===================================================
CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor INT(5) AUTO_INCREMENT PRIMARY KEY,
    nombre TEXT NOT NULL,
    telefono VARCHAR(20),
    direccion TEXT
);

-- ===================================================
-- 🧩 TABLA VENTAS (CORREGIDA)
-- ===================================================
DROP TABLE IF EXISTS ventas;

CREATE TABLE ventas (
    id_venta INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE DEFAULT CURRENT_DATE,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    total DECIMAL(6,2) NOT NULL,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
) ENGINE=InnoDB;


-- ===================================================
-- 🧩 TABLA COMPRAS (CORREGIDA)
-- ===================================================
DROP TABLE IF EXISTS compras;

CREATE TABLE compras (
    id_compra INT(5) AUTO_INCREMENT PRIMARY KEY,
    fecha DATE DEFAULT CURRENT_DATE,
    id_proveedor INT(5),
    id_producto INT(5),
    cantidad DECIMAL(6,2),
    total DECIMAL(6,2),
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
) ENGINE=InnoDB;


-- ===================================================
-- 🧩 TABLA REPORTES
-- ===================================================
CREATE TABLE IF NOT EXISTS reportes (
    id_reporte INT(5) AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(50),
    descripcion TEXT,
    fecha DATE DEFAULT CURRENT_DATE
);

-- ===================================================
-- 🧩 TABLA PEDIDOS
-- ===================================================
DROP TABLE IF EXISTS pedidos;

CREATE TABLE pedidos (
    id_pedido INT(5) AUTO_INCREMENT PRIMARY KEY,
    cliente TEXT NOT NULL,
    producto TEXT NOT NULL,
    cantidad DECIMAL(6,2) NOT NULL,
    precio DECIMAL(6,2) NOT NULL,
    anticipo DECIMAL(6,2) DEFAULT 0,
    total DECIMAL(6,2) NOT NULL,
    restante DECIMAL(6,2) NOT NULL,
    fecha_entrega DATE NOT NULL,
    estado TEXT DEFAULT 'Pendiente'
);
