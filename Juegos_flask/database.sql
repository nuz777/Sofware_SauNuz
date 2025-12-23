CREATE DATABASE juegos_db;
USE juegos_db;

CREATE TABLE admin (
  id INT AUTO_INCREMENT PRIMARY KEY,
  usuario VARCHAR(50) NOT NULL,
  password VARCHAR(255) NOT NULL
);

CREATE TABLE juegos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100),
  link TEXT,
  imagen TEXT
);

-- ADMIN DE EJEMPLO (password: admin123)
INSERT INTO admin (usuario, password)
VALUES ('admin', SHA2('admin123',256));
