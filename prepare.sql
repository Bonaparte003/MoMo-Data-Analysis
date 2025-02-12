DROP DATABASE IF EXISTS MOMO;
CREATE USER IF NOT EXISTS 'Group5'@'localhost' IDENTIFIED BY 'Group5Go';
CREATE DATABASE IF NOT EXISTS MOMO;
GRANT ALL PRIVILEGES ON MOMO.* TO 'Group5'@'localhost';
FLUSH PRIVILEGES;
USE MOMO;

-- Create tables if they do not exist
CREATE TABLE IF NOT EXISTS airtime (
    TxId VARCHAR(250) PRIMARY KEY NOT NULL,
    Amount INT, 
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME, 
    Type VARCHAR(250), 
    Balance INT, 
    Fee INT
);

CREATE TABLE IF NOT EXISTS bundles (
    TxId VARCHAR(250) PRIMARY KEY NOT NULL,
    Amount INT,
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME,
    Type VARCHAR(250),
    Balance INT,
    Fee INT
);

CREATE TABLE IF NOT EXISTS cashpower (
    TxId VARCHAR(250) PRIMARY KEY NOT NULL,
    TOKEN VARCHAR(250),
    Amount INT,
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME,
    Type VARCHAR(250),
    Balance INT,
    Fee INT
);

CREATE TABLE IF NOT EXISTS payments (
    TxId VARCHAR(250) PRIMARY KEY NOT NULL,
    RECEIVER VARCHAR(250),
    AMOUNT INT,
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME,
    Type VARCHAR(250),
    Balance INT,
    Fee INT
);

CREATE TABLE IF NOT EXISTS reversedtransactions (
    RECEIVER VARCHAR(250),
    AMOUNT INT,
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME,
    Type VARCHAR(250),
    BALANCE INT,
    PHONE_NUMBER VARCHAR(250),
    FEE INT
);

CREATE TABLE IF NOT EXISTS failedtransactions (
    RECEIVER VARCHAR(250),
    AMOUNT INT,
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME,
    Type TEXT,
    FEE INT
);

CREATE TABLE IF NOT EXISTS thirdparty (
    SENDER VARCHAR(250),
    AMOUNT INT,
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME,
    Type VARCHAR(250),
    Balance INT,
    Fee INT
);

CREATE TABLE IF NOT EXISTS withdraw (
    AGENT VARCHAR(250),
    AMOUNT INT,
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME,
    Type VARCHAR(250),
    Balance INT,
    Fee INT
);

CREATE TABLE IF NOT EXISTS nontransaction (
    NUMBER INT
);

CREATE TABLE IF NOT EXISTS incomingmoney (
    SENDER VARCHAR(250),
    AMOUNT INT,
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME,
    Type VARCHAR(250),
    Balance INT,
    Fee INT
);

CREATE TABLE IF NOT EXISTS transfer (
    RECEIVER VARCHAR(250),
    PHONE_NUMBER VARCHAR(250),
    AMOUNT INT,
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME,
    Type VARCHAR(250),
    Balance INT,
    Fee INT
);

CREATE TABLE IF NOT EXISTS deposit (
    AMOUNT INT,
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME,
    Type VARCHAR(250),
    Balance INT,
    Fee INT
);

CREATE TABLE IF NOT EXISTS codeholders (
    RECEIVER VARCHAR(250),
    CODE INT,
    TxId VARCHAR(250) PRIMARY KEY NOT NULL,
    AMOUNT INT,
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME,
    Type VARCHAR(250),
    Balance INT,
    Fee INT
);