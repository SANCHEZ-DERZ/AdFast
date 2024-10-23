CREATE TABLE sources (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	NAME VARCHAR(100) NOT NULL,
	tg_id VARCHAR(100) NOT NULL,
	link VARCHAR(2048) NOT NULL,
	platform VARCHAR(100) NOT NULL,
	category SET('Fashion', 'IT', 'Travel', 'Busines', 'Beauty') NOT NULL
);