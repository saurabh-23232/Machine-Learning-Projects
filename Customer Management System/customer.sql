-- 1. Create the Database
CREATE DATABASE CustomerManagementSystem;
USE CustomerManagementSystem;

-- 2. Create the Customers Table
CREATE TABLE Customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(15),
    address TEXT,
    city VARCHAR(50),
    state VARCHAR(50),
    postal_code VARCHAR(10),
    country VARCHAR(50),
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
INSERT INTO Customers (first_name, last_name, email, phone_number, address, city, state, postal_code, country)
VALUES ('Jane', 'Doe', 'janedoe@example.com', '0987654321', '456 Maple St', 'Metropolis', 'NY', '10001', 'USA');

SELECT * FROM Customers WHERE email = 'janedoe@example.com';


-- 3. Create the CustomerInteractions Table
CREATE TABLE CustomerInteractions (
    interaction_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    interaction_type ENUM('Email', 'Phone Call', 'Meeting', 'Other') NOT NULL,
    interaction_date DATETIME NOT NULL,
    notes TEXT,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
        ON DELETE CASCADE
);

-- 4. Create the Users Table
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('Admin', 'Manager', 'User') DEFAULT 'User',
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Create Indexes for Performance Optimization
CREATE INDEX idx_customer_name ON Customers (first_name, last_name);
CREATE INDEX idx_interaction_date ON CustomerInteractions (interaction_date);
CREATE INDEX idx_user_role ON Users (role);

-- 6. Insert Sample Data into Customers Table
INSERT INTO Customers (first_name, last_name, email, phone_number, city, state, country)
VALUES ('John', 'Doe', 'johndoe@example.com', '1234567890', 'New York', 'NY', 'USA');

-- 7. Insert Sample Data into CustomerInteractions Table
INSERT INTO CustomerInteractions (customer_id, interaction_type, interaction_date, notes)
VALUES (1, 'Email', '2024-08-24 10:00:00', 'Discussed the new service offerings.');

-- 8. Insert Sample Data into Users Table
INSERT INTO Users (username, password_hash, role)
VALUES ('admin', SHA2('password123', 256), 'Admin');
