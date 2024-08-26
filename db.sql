CREATE DATABASE IF NOT EXISTS inpac;

USE inpac;

CREATE TABLE Device (
    id INT AUTO_INCREMENT PRIMARY KEY,
    model VARCHAR(50),
    serial_number VARCHAR(50),
    device_name VARCHAR(50),
    manufacturer VARCHAR(50),
    firmware_version VARCHAR(50),
    device_location VARCHAR(50),
    last_log_id INT DEFAULT -1
);

CREATE TABLE User (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL,
    ip_login VARCHAR(50),
    last_login DATETIME,
    permission TINYINT(1) DEFAULT 0
);

CREATE TABLE Device_Log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_id INT,
    user_id INT NOT NULL,
    date DATETIME,
    action VARCHAR(50),
    description TEXT,
    FOREIGN KEY (device_id) REFERENCES Device(id),
    FOREIGN KEY (user_id) REFERENCES User(id)
);

-- add placeholders indicating empty values
INSERT INTO
    User (id, email)
VALUES
    (-1, 'placeholder');

INSERT INTO
    Device (id)
VALUES
    (-1);

INSERT INTO
    Device_Log (Device_id, User_id, Date, Action, Description)
VALUES
    (-1, -1, NOW(), 'No prior log', 'No prior log');