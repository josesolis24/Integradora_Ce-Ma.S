-- ===================================================
-- 🚀 CREACIÓN DE LA BASE DE DATOS
-- ===================================================
DROP DATABASE IF EXISTS inventario_cema;
CREATE DATABASE inventario_cema;
USE inventario_cema;

-- ===================================================
-- 🧩 MOTOR POR DEFECTO (GARANTIZA INNODB)
-- ===================================================
SET default_storage_engine = INNODB;

-- ===================================================
-- 🧩 TABLA USUARIOS
-- ===================================================
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    nombre_completo TEXT
) ENGINE=InnoDB;

INSERT INTO usuarios (username, password, nombre_completo)
VALUES ('admin', '1234', 'Administrador General')
ON DUPLICATE KEY UPDATE username = username;

-- ===================================================
-- 🧩 TABLA CATEGORÍAS
-- ===================================================
CREATE TABLE categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre TEXT NOT NULL,
   ) ENGINE=InnoDB;

-- ===================================================
-- 🧩 TABLA PROVEEDORES
-- ===================================================
CREATE TABLE proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre TEXT NOT NULL,
    telefono VARCHAR(20),
    direccion TEXT
) ENGINE=InnoDB;

-- ===================================================
-- 🧩 TABLA PRODUCTOS
-- ===================================================
CREATE TABLE productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL,
    stock INT DEFAULT 0,
    id_categoria INT,
    id_proveedor INT,

    CONSTRAINT fk_producto_categoria
        FOREIGN KEY (id_categoria)
        REFERENCES categorias(id_categoria)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

    CONSTRAINT fk_producto_proveedor
        FOREIGN KEY (id_proveedor)
        REFERENCES proveedores(id_proveedor)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ===================================================
-- 🧩 TABLA VENTAS
-- ===================================================
CREATE TABLE ventas (
    id_venta INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE DEFAULT CURRENT_DATE,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    total DECIMAL(10,2) NOT NULL,

    CONSTRAINT fk_venta_producto
        FOREIGN KEY (id_producto)
        REFERENCES productos(id_producto)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ===================================================
-- 🧩 TABLA COMPRAS
-- ===================================================
CREATE TABLE compras (
    id_compra INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE DEFAULT CURRENT_DATE,
    id_proveedor INT,
    id_producto INT,
    cantidad DECIMAL(10,2),
    total DECIMAL(10,2),

    CONSTRAINT fk_compra_proveedor
        FOREIGN KEY (id_proveedor)
        REFERENCES proveedores(id_proveedor)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

    CONSTRAINT fk_compra_producto
        FOREIGN KEY (id_producto)
        REFERENCES productos(id_producto)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ===================================================
-- 🧩 TABLA REPORTES
-- ===================================================
CREATE TABLE reportes (
    id_reporte INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(50),
    descripcion TEXT,
    fecha DATE DEFAULT CURRENT_DATE
) ENGINE=InnoDB;

-- ===================================================
-- 🧩 TABLA PEDIDOS
-- ===================================================
CREATE TABLE pedidos (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    cliente TEXT NOT NULL,
    producto TEXT NOT NULL,
    cantidad DECIMAL(10,2) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    anticipo DECIMAL(10,2) DEFAULT 0,
    total DECIMAL(10,2) NOT NULL,
    restante DECIMAL(10,2) NOT NULL,
    fecha_entrega DATE NOT NULL,
    estado TEXT DEFAULT 'Pendiente'
) ENGINE=InnoDB;
