CREATE DATABASE IF NOT EXISTS FinancialAnalysis;
USE FinancialAnalysis;

CREATE TABLE Prices (
    price_id INT AUTO_INCREMENT PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    timestamp DATETIME NOT NULL,
    open DECIMAL(15,2),
    high DECIMAL(15,2),
    low DECIMAL(15,2),
    close DECIMAL(15,2),
    volume DECIMAL(15,2),
    volume_from DECIMAL(15,2),
    INDEX idx_ticker (ticker),
    INDEX idx_timestamp (timestamp)
);

CREATE TABLE News (
    news_id INT AUTO_INCREMENT PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    timestamp DATETIME NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    source VARCHAR(50),
    INDEX idx_ticker (ticker),
    INDEX idx_timestamp (timestamp)
);

CREATE TABLE PriceNews (
    price_id INT NOT NULL,
    news_id INT NOT NULL,
    PRIMARY KEY (price_id, news_id),
    FOREIGN KEY (price_id) REFERENCES Prices(price_id) ON DELETE CASCADE,
    FOREIGN KEY (news_id) REFERENCES News(news_id) ON DELETE CASCADE,
    INDEX idx_price_id (price_id),
    INDEX idx_news_id (news_id)
);

CREATE TABLE ForexData (
    forex_id INT AUTO_INCREMENT PRIMARY KEY,
    pair VARCHAR(10) NOT NULL,
    timestamp DATETIME NOT NULL,
    open DECIMAL(15,6),
    high DECIMAL(15,6),
    low DECIMAL(15,6),
    rate DECIMAL(15,6),
    INDEX idx_pair (pair),
    INDEX idx_timestamp (timestamp)
);

CREATE TABLE EconomicData (
    timestamp DATE PRIMARY KEY,
    inflation_rate DECIMAL(5,2),
    interest_rate DECIMAL(5,2),
    unemployment_rate DECIMAL(5,2),
    treasury_10y DECIMAL(5,2),
    treasury_2y DECIMAL(5,2),
    yield_spread_10y_2y DECIMAL(5,2),
    usd_aud_rate DECIMAL(5,2),
    INDEX idx_timestamp (timestamp)
);