-- Create database
CREATE DATABASE IF NOT EXISTS webbserv_injection_demo;
USE webbserv_injection_demo;

-- Create users table
CREATE TABLE `users` (
    `id` INT NOT NULL AUTO_INCREMENT, 
    `username` VARCHAR(100) NOT NULL, 
    `password` VARCHAR(100) NOT NULL, 
    `name` VARCHAR(250) NOT NULL, 
    `email` VARCHAR(250) NOT NULL, 
    PRIMARY KEY (`id`), 
    UNIQUE `username_unique` (`username`), 
    UNIQUE `email_unique` (`email`)
);

-- Insert a sample user for testing
-- Username: admin, Password: admin123
INSERT INTO `users` (`username`, `password`, `name`, `email`) 
VALUES ('admin', 'admin123', 'Administrator', 'admin@example.com');

-- Insert another sample user
-- Username: user1, Password: password
INSERT INTO `users` (`username`, `password`, `name`, `email`) 
VALUES ('user1', 'password', 'Test User', 'user1@example.com');

-- Username: john_doe, Password: secure123
INSERT INTO `users` (`username`, `password`, `name`, `email`) 
VALUES ('john_doe', 'secure123', 'John Doe', 'john.doe@example.com');

-- Username: jane_smith, Password: mypass456
INSERT INTO `users` (`username`, `password`, `name`, `email`) 
VALUES ('jane_smith', 'mypass456', 'Jane Smith', 'jane.smith@example.com');

-- Username: bob_wilson, Password: bobpass789
INSERT INTO `users` (`username`, `password`, `name`, `email`) 
VALUES ('bob_wilson', 'bobpass789', 'Bob Wilson', 'bob.wilson@example.com');

INSERT INTO `users` (`username`, `password`, `name`, `email`) 
VALUES ('administrator', 'superhemligtlångtlösenord', 'Super Administrator', 'administrator@example.com');
