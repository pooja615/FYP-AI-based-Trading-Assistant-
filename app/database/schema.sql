-- Create Database
CREATE DATABASE IF NOT EXISTS tradesync;
USE tradesync;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    User_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    role VARCHAR(20) DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE
);

-- Stock Symbols Table
CREATE TABLE IF NOT EXISTS symbols (
    Symbol_ID INT AUTO_INCREMENT PRIMARY KEY,
    Code VARCHAR(20) UNIQUE NOT NULL,
    Name VARCHAR(200) NOT NULL,
    Exchange VARCHAR(50) DEFAULT 'NEPSE',
    sector VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Stock Prices Table
CREATE TABLE IF NOT EXISTS prices (
    Price_ID INT AUTO_INCREMENT PRIMARY KEY,
    Symbol_ID INT NOT NULL,
    Date DATE NOT NULL,
    Open DECIMAL(10, 2),
    High DECIMAL(10, 2),
    Low DECIMAL(10, 2),
    Close DECIMAL(10, 2),
    Volume INT,
    FOREIGN KEY (Symbol_ID) REFERENCES symbols(Symbol_ID),
    UNIQUE KEY unique_symbol_date (Symbol_ID, Date)
);

-- Simulated Trades Table
CREATE TABLE IF NOT EXISTS trade_sims (
    Trade_id INT AUTO_INCREMENT PRIMARY KEY,
    User_id INT NOT NULL,
    Symbol_id INT NOT NULL,
    Action VARCHAR(10) NOT NULL,
    Price DECIMAL(10, 2) NOT NULL,
    Quantity INT NOT NULL,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    Profit_loss DECIMAL(10, 2) DEFAULT 0,
    FOREIGN KEY (User_id) REFERENCES users(User_ID),
    FOREIGN KEY (Symbol_id) REFERENCES symbols(Symbol_ID)
);

-- Predictions Table
CREATE TABLE IF NOT EXISTS prediction (
    Pred_ID INT AUTO_INCREMENT PRIMARY KEY,
    Symbol_ID INT NOT NULL,
    User_ID INT,
    Date_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    Model_type VARCHAR(50),
    Prediction_value DECIMAL(10, 2),
    Confidence DECIMAL(5, 2),
    Trend VARCHAR(20),
    Notes TEXT,
    FOREIGN KEY (Symbol_ID) REFERENCES symbols(Symbol_ID),
    FOREIGN KEY (User_ID) REFERENCES users(User_ID)
);

-- Alerts Table
CREATE TABLE IF NOT EXISTS alerts (
    Alert_ID INT AUTO_INCREMENT PRIMARY KEY,
    User_ID INT NOT NULL,
    Symbol_ID INT,
    Alert_type VARCHAR(50),
    Threshold_value DECIMAL(10, 2),
    Is_triggered BOOLEAN DEFAULT FALSE,
    Created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (User_ID) REFERENCES users(User_ID),
    FOREIGN KEY (Symbol_ID) REFERENCES symbols(Symbol_ID)
);

-- Insert Sample Stock Data
INSERT INTO symbols (Code, Name, Exchange, sector) VALUES
('NABIL', 'Nabil Bank Limited', 'NEPSE', 'Banking'),
('NICA', 'Nepal Investment Bank', 'NEPSE', 'Banking'),
('GBIME', 'Global IME Bank', 'NEPSE', 'Banking'),
('NTC', 'Nepal Telecom', 'NEPSE', 'Telecommunication'),
('NPL', 'Nepal Petroleum', 'NEPSE', 'Manufacturing');

-- Insert Sample Admin User (password: admin123)
INSERT INTO users (Name, Email, password_hash, role) VALUES
('Admin', 'admin@tradesync.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzS3MebAJu', 'admin'),
('Demo User', 'user@tradesync.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzS3MebAJu', 'user');