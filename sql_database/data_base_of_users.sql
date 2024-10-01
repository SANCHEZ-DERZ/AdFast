DROP TABLE if EXISTS users_adfast;
SET foreign_key_checks = 0;
SET foreign_key_checks = 1;
CREATE TABLE users_adfast (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    name VARCHAR(255) NULL,
    user_id INT NOT NULL,
    UNIQUE KEY USER (NAME, user_id)
);