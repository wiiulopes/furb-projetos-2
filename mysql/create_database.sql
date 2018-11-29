CREATE DATABASE vision;
USE vision;
CREATE TABLE coordenada(
id INT(6) AUTO_INCREMENT,
lat DECIMAL(10, 8) NOT NULL,
lng DECIMAL(11, 8) NOT NULL,
ponto_interesse varchar(50),
PRIMARY KEY (id));

CREATE TABLE posicao_atual(
id INT(6) AUTO_INCREMENT,
lat DECIMAL(10, 8) NOT NULL,
lng DECIMAL(11, 8) NOT NULL,
PRIMARY KEY (id));

