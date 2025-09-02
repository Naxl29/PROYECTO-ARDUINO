/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE DATABASE IF NOT EXISTS `arduino` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `arduino`;

CREATE TABLE IF NOT EXISTS `objetos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `objeto` varchar(50) NOT NULL,
  `potencia_w` int NOT NULL,
  `consumo_wh` float NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `objetos` (`id`, `objeto`, `potencia_w`, `consumo_wh`) VALUES
	(1, 'LUZ SALA', 60, 0.06),
	(2, 'LUZ COCINA', 60, 0.06),
	(3, 'LUZ HABITACIÓN', 60, 0.06),
	(4, 'LUZ BAÑO', 60, 0.06),
	(5, 'AIRE ACONDICIONADO', 800, 0.8),
	(6, 'LAVADORA', 500, 0.5),
	(7, 'NEVERA', 200, 0.2),
	(8, 'TELEVISOR', 150, 0.15);

CREATE TABLE IF NOT EXISTS `reportes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `id_objeto` int NOT NULL,
  `fecha` datetime NOT NULL,
  `duracion_minutos` float NOT NULL,
  `estado` tinyint(1) NOT NULL,
  `gasto` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_reportes_usuarios` (`id_usuario`),
  KEY `FK_reportes_objetos` (`id_objeto`),
  CONSTRAINT `FK_reportes_objetos` FOREIGN KEY (`id_objeto`) REFERENCES `objetos` (`id`),
  CONSTRAINT `FK_reportes_usuarios` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `reportes` (`id`, `id_usuario`, `id_objeto`, `fecha`, `duracion_minutos`, `estado`, `gasto`) VALUES
	(1, 1, 1, '2025-09-02 07:25:28', 20, 1, 0.02),
	(2, 1, 5, '2025-09-02 10:15:00', 30, 1, 0.4),
	(3, 1, 5, '2025-09-02 10:15:00', 30, 1, 0.4);

CREATE TABLE IF NOT EXISTS `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `rol` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `roles` (`id`, `rol`) VALUES
	(1, 'ADMIN'),
	(2, 'USER'),
	(3, 'CHILD');

CREATE TABLE IF NOT EXISTS `roles_usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `id_rol` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK__usuarios` (`id_usuario`),
  KEY `FK__roles` (`id_rol`),
  CONSTRAINT `FK__roles` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id`),
  CONSTRAINT `FK__usuarios` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `roles_usuarios` (`id`, `id_usuario`, `id_rol`) VALUES
	(1, 1, 1),
	(2, 2, 2),
	(3, 3, 3);

CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario` varchar(50) NOT NULL,
  `contrasena` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `usuarios` (`id`, `usuario`, `contrasena`) VALUES
	(1, 'ADMIN', '123456'),
	(2, 'USER', '123456'),
	(3, 'CHILD', '123456');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
