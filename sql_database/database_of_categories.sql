DROP TABLE if EXISTS sources;
CREATE TABLE sources (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	NAME VARCHAR(100) NOT NULL,
	link VARCHAR(2048) NOT NULL,
	platform SET('Instagam', 'Telegram', 'Tik-tok', 'Vk', 'YouTube', 'Yandex Dzen') NULL,
	subscribers INT NOT NULL,
	category SET('Fashion', 'IT', 'Travel', 'Busines', 'Beauty') NOT NULL,
	UNIQUE KEY name (name)
);
