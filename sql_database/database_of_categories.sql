DROP TABLE if EXISTS sources;
CREATE TABLE sources (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	NAME VARCHAR(100) NOT NULL,
	link VARCHAR(2048) NOT NULL,
	platform SET('Instagram', 'Telegram', 'TikTok', 'Vk', 'YouTube', 'Yandex Dzen') NULL,
	subscribers INT NOT NULL,
	category SET('Fashion', 'IT', 'Travel', 'Busines', 'Beauty') NOT NULL,
	description VARCHAR(2048) NOT NULL,
	contact varchar(2048) not null,
	UNIQUE KEY name (name)
);
