-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 10-12-2025 a las 21:46:45
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `inventario_cema`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias`
--

CREATE TABLE `categorias` (
  `id_categoria` int(11) NOT NULL,
  `nombre` text NOT NULL,
  `creado_por` varchar(100) DEFAULT NULL,
  `actualizado_por` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `categorias`
--

INSERT INTO `categorias` (`id_categoria`, `nombre`, `creado_por`, `actualizado_por`) VALUES
(1, 'Grande', 'admin', 'admin'),
(2, 'Mediano', 'admin', 'admin'),
(3, 'Chico', 'admin', 'admin'),
(4, 'Camisa Mediana', 'admin', 'admin'),
(5, 'Playera Chica', 'admin', 'admin'),
(6, 'playera grande', 'admin', 'admin'),
(7, 'sueter grande', 'admin', 'admin'),
(10, 'Sudadera Mediana', 'Luis', 'Luis'),
(11, 'Gorra  Negro', 'admin', 'admin'),
(12, 'Frasada Azul', 'admin', 'admin'),
(13, '500ml', 'admin', 'admin'),
(14, '80ml', 'admin', 'admin');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `compras`
--

CREATE TABLE `compras` (
  `id_compra` int(11) NOT NULL,
  `fecha` date DEFAULT curdate(),
  `id_proveedor` int(11) DEFAULT NULL,
  `proveedor_nombre` text DEFAULT NULL,
  `id_producto` int(11) NOT NULL,
  `nombre_producto` text NOT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `total` decimal(6,2) DEFAULT NULL,
  `id_categoria` int(11) DEFAULT NULL,
  `nombre_categoria` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `compras`
--

INSERT INTO `compras` (`id_compra`, `fecha`, `id_proveedor`, `proveedor_nombre`, `id_producto`, `nombre_producto`, `cantidad`, `total`, `id_categoria`, `nombre_categoria`) VALUES
(4, '2025-12-04', NULL, 'Ivan legaspi', 17, 'Termo Rojo', 50, 5000.00, 1, 'Grande'),
(5, '2025-12-04', NULL, 'Ivan legaspi', 17, 'Termo Rojo', 50, 5000.00, 1, 'Grande'),
(6, '2025-12-08', NULL, 'Ivan legaspi', 17, 'Termo Rojo', 100, 9999.99, 3, 'Chico'),
(7, '2025-12-09', 2, 'Casa Xavier', 20, 'Playera negra', 100, 9999.99, 2, 'Mediano'),
(9, '2025-12-10', 2, 'Casa Xavier', 17, 'Termo Rojo', 20, 3000.00, 13, '500ml'),
(10, '2025-12-10', 2, 'Casa Xavier', 18, 'Termo Rosa', 2, 240.00, 13, '500ml');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedidos`
--

CREATE TABLE `pedidos` (
  `id_pedido` int(11) NOT NULL,
  `cliente` text NOT NULL,
  `producto` int(11) NOT NULL,
  `nombre_producto` text NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio` decimal(6,2) NOT NULL,
  `anticipo` decimal(6,2) DEFAULT 0.00,
  `total` decimal(6,2) NOT NULL,
  `restante` decimal(6,2) NOT NULL,
  `fecha_entrega` date NOT NULL,
  `estado` text DEFAULT 'Pendiente',
  `creado_por` varchar(50) DEFAULT NULL,
  `actualizado_por` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pedidos`
--

INSERT INTO `pedidos` (`id_pedido`, `cliente`, `producto`, `nombre_producto`, `cantidad`, `precio`, `anticipo`, `total`, `restante`, `fecha_entrega`, `estado`, `creado_por`, `actualizado_por`) VALUES
(8, 'pepe', 17, 'Termo Rojo', 50, 1500.00, 9999.99, 9999.99, 0.00, '2025-12-20', 'Pagado', 'admin', 'admin'),
(9, 'pedro', 17, 'Termo Rojo', 50, 150.00, 7500.00, 7500.00, 0.00, '2026-01-20', 'Pagado', 'admin', 'admin'),
(10, 'Luis', 17, 'Termo Rojo', 14, 100.00, 1400.00, 1400.00, 0.00, '2025-12-20', 'Pagado', 'admin', 'admin'),
(11, 'Jose', 17, 'Termo Rojo', 16, 150.00, 2400.00, 2400.00, 0.00, '2025-12-20', 'Pagado', 'admin', 'admin'),
(12, 'Rosario', 18, 'Termo Rosa', 80, 120.00, 9600.00, 9600.00, 0.00, '2026-01-15', 'Pagado', 'admin', 'admin'),
(13, 'Nayeli', 19, 'Playera blanca', 5, 200.00, 100.00, 1000.00, 900.00, '2025-12-12', 'Pendiente', 'admin', 'admin'),
(14, 'Sanches', 17, 'Termo Rojo', 10, 150.00, 500.00, 1500.00, 1000.00, '2025-12-21', 'Pendiente', 'admin', 'admin'),
(15, 'Rodriguez', 20, 'Playera negra', 50, 150.00, 6500.00, 7500.00, 1000.00, '2025-12-30', 'Pendiente', 'admin', 'admin'),
(17, 'Panfila', 17, 'Termo Rojo', 2, 150.00, 300.00, 300.00, 0.00, '2025-12-20', 'Pagado', 'admin', 'admin');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id_producto` int(11) NOT NULL,
  `nombre` text NOT NULL,
  `descripcion` text DEFAULT NULL,
  `precio` decimal(6,2) NOT NULL,
  `stock` int(11) DEFAULT 0,
  `id_categoria` int(11) DEFAULT NULL,
  `id_proveedor` int(11) DEFAULT NULL,
  `creado_por` varchar(50) DEFAULT NULL,
  `actualizado_por` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id_producto`, `nombre`, `descripcion`, `precio`, `stock`, `id_categoria`, `id_proveedor`, `creado_por`, `actualizado_por`) VALUES
(17, 'Termo Rojo', 'Niño', 150.00, 8, 1, 2, 'admin', 'admin'),
(18, 'Termo Rosa', 'Niña', 120.00, 20, 3, 2, 'admin', 'Luis'),
(19, 'Playera blanca', 'Unisex', 150.00, 15, 1, 2, 'admin', 'admin'),
(20, 'Playera negra', 'Navidena', 160.00, 50, 5, 2, 'admin', 'admin');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedores`
--

CREATE TABLE `proveedores` (
  `id_proveedor` int(11) NOT NULL,
  `nombre` text NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `direccion` text DEFAULT NULL,
  `correo_electronico` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `proveedores`
--

INSERT INTO `proveedores` (`id_proveedor`, `nombre`, `telefono`, `direccion`, `correo_electronico`) VALUES
(2, 'Casa Xavier', '81 83709196', 'Col. Rincón de Santa Maria, Monterrey, N.L', 'ventas1@sparviero.com.mx'),
(3, 'Martin', '618276643', 'Durango Dgo', 'martin@gmail.com');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reportes_generados`
--

CREATE TABLE `reportes_generados` (
  `id_reporte` int(11) NOT NULL,
  `nombre_reporte` varchar(255) DEFAULT NULL,
  `total_registros` int(11) DEFAULT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp(),
  `usuario` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `reportes_generados`
--

INSERT INTO `reportes_generados` (`id_reporte`, `nombre_reporte`, `total_registros`, `fecha`, `usuario`) VALUES
(1, 'Compras registradas', 3, '2025-12-08 17:51:55', 'admin'),
(2, 'Proveedores registrados', 1, '2025-12-08 17:58:55', 'admin'),
(3, 'Pedidos registrados', 5, '2025-12-08 17:59:06', 'admin'),
(4, 'Compras registradas', 3, '2025-12-08 17:59:09', 'admin'),
(5, 'Ventas registradas', 4, '2025-12-08 17:59:13', 'admin'),
(6, 'Categorias registradas', 10, '2025-12-08 17:59:15', 'admin'),
(7, 'Productos registrados', 2, '2025-12-08 17:59:18', 'admin'),
(8, 'Proveedores registrados', 1, '2025-12-08 18:06:28', 'admin'),
(9, 'Pedidos registrados', 6, '2025-12-08 18:39:59', 'admin'),
(10, 'Productos registrados', 3, '2025-12-09 01:13:39', 'admin'),
(11, 'Categorias registradas', 10, '2025-12-09 01:13:43', 'admin'),
(12, 'Ventas registradas', 5, '2025-12-09 01:13:45', 'admin'),
(13, 'Compras registradas', 4, '2025-12-09 01:13:48', 'admin'),
(14, 'Pedidos registrados', 6, '2025-12-09 01:13:52', 'admin'),
(15, 'Proveedores registrados', 1, '2025-12-09 01:13:54', 'admin'),
(16, 'Pedidos registrados', 7, '2025-12-09 07:17:59', 'admin'),
(17, 'Productos registrados', 5, '2025-12-09 16:23:41', 'admin'),
(18, 'Productos registrados', 5, '2025-12-10 03:49:17', 'admin'),
(19, 'Categorias registradas', 11, '2025-12-10 03:49:20', 'admin'),
(20, 'Ventas registradas', 7, '2025-12-10 03:49:23', 'admin'),
(21, 'Compras registradas', 5, '2025-12-10 03:49:39', 'admin'),
(22, 'Pedidos registrados', 10, '2025-12-10 03:49:41', 'admin'),
(23, 'Proveedores registrados', 1, '2025-12-10 03:49:44', 'admin'),
(24, 'Categorias registradas', 11, '2025-12-10 03:52:01', 'admin'),
(25, 'Ventas registradas', 7, '2025-12-10 15:18:45', 'admin'),
(26, 'Ventas registradas', 7, '2025-12-10 15:19:02', 'admin'),
(27, 'Ventas registradas', 6, '2025-12-10 15:24:33', 'admin'),
(28, 'Ventas registradas', 6, '2025-12-10 16:42:37', 'admin'),
(29, 'Ventas registradas', 6, '2025-12-10 17:39:12', 'admin');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `rol` text DEFAULT 'invitado'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `username`, `password`, `rol`) VALUES
(1, 'admin', '1234', 'administrador General'),
(2, 'Luis', '1234', 'Empleado'),
(3, 'Pedro', '1234', 'Invitado'),
(4, 'Luisa', '1234', 'Empleado');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas`
--

CREATE TABLE `ventas` (
  `id_venta` int(11) NOT NULL,
  `fecha` datetime DEFAULT current_timestamp(),
  `id_producto` int(11) NOT NULL,
  `nombre_producto` text NOT NULL,
  `cantidad` int(11) NOT NULL CHECK (`cantidad` > 0),
  `total` decimal(10,2) NOT NULL,
  `creado_por` varchar(50) DEFAULT NULL,
  `actualizado_por` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ventas`
--

INSERT INTO `ventas` (`id_venta`, `fecha`, `id_producto`, `nombre_producto`, `cantidad`, `total`, `creado_por`, `actualizado_por`) VALUES
(12, '2025-12-04 23:03:46', 17, 'Termo Rojo', 50, 5000.00, 'admin', 'admin'),
(13, '2025-12-04 23:44:36', 17, 'Termo Rojo', 10, 1000.00, 'admin', 'admin'),
(14, '2025-12-07 10:43:29', 18, 'Termo Rosa', 85, 10200.00, NULL, 'admin'),
(15, '2025-12-07 10:54:53', 17, 'Termo Rojo', 70, 10500.00, NULL, 'admin'),
(16, '2025-12-08 12:44:05', 19, 'Playera blanca', 13, 1950.00, 'admin', 'admin'),
(28, '2025-12-09 21:46:06', 17, 'Termo Rojo', 2, 300.00, 'admin', 'admin');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `categorias`
--
ALTER TABLE `categorias`
  ADD PRIMARY KEY (`id_categoria`);

--
-- Indices de la tabla `compras`
--
ALTER TABLE `compras`
  ADD PRIMARY KEY (`id_compra`),
  ADD KEY `fk_compra_proveedor` (`id_proveedor`),
  ADD KEY `fk_compra_producto` (`id_producto`);

--
-- Indices de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD PRIMARY KEY (`id_pedido`),
  ADD KEY `fk_pedido_producto` (`producto`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id_producto`),
  ADD KEY `fk_producto_categoria` (`id_categoria`),
  ADD KEY `fk_producto_proveedor` (`id_proveedor`);

--
-- Indices de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  ADD PRIMARY KEY (`id_proveedor`);

--
-- Indices de la tabla `reportes_generados`
--
ALTER TABLE `reportes_generados`
  ADD PRIMARY KEY (`id_reporte`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indices de la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD PRIMARY KEY (`id_venta`),
  ADD KEY `fk_venta_producto` (`id_producto`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `categorias`
--
ALTER TABLE `categorias`
  MODIFY `id_categoria` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT de la tabla `compras`
--
ALTER TABLE `compras`
  MODIFY `id_compra` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  MODIFY `id_pedido` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id_producto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  MODIFY `id_proveedor` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `reportes_generados`
--
ALTER TABLE `reportes_generados`
  MODIFY `id_reporte` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `ventas`
--
ALTER TABLE `ventas`
  MODIFY `id_venta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `compras`
--
ALTER TABLE `compras`
  ADD CONSTRAINT `fk_compra_producto` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_compra_proveedor` FOREIGN KEY (`id_proveedor`) REFERENCES `proveedores` (`id_proveedor`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Filtros para la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD CONSTRAINT `fk_pedido_producto` FOREIGN KEY (`producto`) REFERENCES `productos` (`id_producto`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `productos`
--
ALTER TABLE `productos`
  ADD CONSTRAINT `fk_producto_categoria` FOREIGN KEY (`id_categoria`) REFERENCES `categorias` (`id_categoria`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_producto_proveedor` FOREIGN KEY (`id_proveedor`) REFERENCES `proveedores` (`id_proveedor`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Filtros para la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD CONSTRAINT `fk_venta_producto` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
