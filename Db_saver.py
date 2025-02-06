# import sqlite3
# import json
# import os

# def save_to_db(json_file_path, db_path):
#     table_name = os.path.splitext(os.path.basename(json_file_path))[0]

#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

#     with open(json_file_path, 'r', encoding='utf-8') as f:
#         data = json.load(f)

#     if data:
#         columns = data[0].keys()
#         columns_with_types = ", ".join([f"{col} TEXT" for col in columns])
#         cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types})")

#         for entry in data:
#             placeholders = ", ".join(["?" for _ in entry])
#             cursor.execute(f"INSERT INTO {table_name} ({', '.join(entry.keys())}) VALUES ({placeholders})", tuple(entry.values()))

#     conn.commit()
#     conn.close()

# json_files = [
#     'cleaned_incoming_money.json',
#     'cleaned_payments.json',
#     'cleaned_deposit.json',
#     'cleaned_withdraw.json',
#     'cleaned_transfer.json',
#     'cleaned_third_party.json',
#     'cleaned_payment_code_holders.json',
#     'cleaned_cash_power.json',
#     'cleaned_Airtime.json',
#     'cleaned_Bundles.json',
#     'cleaned_rest.json'
# ]

# db_path = 'data.db'

# for json_file in json_files:
#     json_file_path = os.path.join('Data_Categorization', 'Cleaned_Data', json_file)
#     save_to_db(json_file_path, db_path)

# print("Data has been saved to the database")

import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

sqlstatements= [
    """CREATE TABLE IF NOT EXISTS Airtime (
    TxId TEXT PRIMARY KEY NOT NULL,
    Amount INT, 
    CURRENCY TEXT,
    Date DATE,
    TIME DATE, 
    Type TEXT, 
    Balance INT, 
    Fee INT
    );""",
    
    """CREATE TABLE IF NOT EXISTS Bundles(
    TxId TEXT PRIMARY KEY NOT NULL,
    Amount INT,
    CURRENCY TEXT,
    Date DATE,
    TIME DATE,
    Type TEXT,
    Balance INT,
    Fee INT
    );
    """,
    
    """CREATE TABLE IF NOT EXISTS Cash_Power(
    TxId TEXT PRIMARY KEY NOT NULL,
    TOKEN TEXT,
    Amount INT,
    CURRENCY TEXT,
    Date DATE,
    TIME TIME,
    Type TEXT,
    Balance INT,
    Fee INT
    );""",
    
    """CREATE TABLE IF NOT EXISTS Deposit(
    AMOUNT INT,
    CURRENCY TEXT,
    Date DATE,
    TIME TIME,
    Type TEXT,
    Balance INT,
    Fee INT
    );""",
    
    """CREATE TABLE IF NOT EXISTS Incoming_Money(
    SENDER TEXT,
    AMOUNT INT,
    CURRENCY TEXT,
    Date DATE,
    TIME TIME,
    Type TEXT,
    Balance INT,
    Fee INT
    );""",
    
    """CREATE TABLE IF NOT EXISTS Payments(
    TxId TEXT PRIMARY KEY NOT NULL,
    RECIEVER TEXT,
    PHONE_NUMBER TEXT,
    AMOUNT INT,
    CURRENCY TEXT,
    Date DATE,
    TIME TIME,
    Type TEXT,
    Balance INT,
    Fee INT
    );""",
    
    
    """CREATE TABLE IF NOT EXISTS FAILED_TRANSACTIONS(
    TxId TEXT PRIMARY KEY NOT NULL,
    RECIEVER TEXT,
    AMOUNT INT,
    CURRENCY TEXT,
    Date DATE,
    TIME TIME,
    Type TEXT
    );""",
    
    """CREATE TABLE IF NOT EXISTS REVERSED_TRANSACTIONS(
    RECEIVER TEXT,
    AMOUNT INT,
    CURRENCY TEXT,
    Date DATE,
    TIME TIME,
    Type TEXT,
    BALANCE INT
    );""",
    
    
    """CREATE TABLE IF NOT EXISTS THIRD_PARTY(
    TxId TEXT PRIMARY KEY NOT NULL,
    SENDER TEXT,
    AMOUNT INT,
    CURRENCY TEXT,
    Date DATE,
    TIME TIME,
    Type TEXT,
    Balance INT,
    Fee INT
    );""",
    
    
    """CREATE TABLE IF NOT EXISTS Transfer(
    RECEIVER TEXT,
    PHONE_NUMBER TEXT,
    AMOUNT INT,
    CURRENCY TEXT,
    Date DATE,
    TIME TIME,
    Type TEXT,
    Balance INT,
    Fee INT
    );""",
    
    """CREATE TABLE IF NOT EXISTS WITHDRAW(
    TxId TEXT PRIMARY KEY NOT NULL,
    AGENT TEXT,
    AMOUNT INT,
    CURRENCY TEXT,
    Date DATE,
    TIME TIME,
    Type TEXT,
    Balance INT,
    Fee INT
    );""",
    
    """CREATE TABLE IF NOT EXISTS NON_TRANSACTION(
    NUMBER INT);"""
]

for statement in sqlstatements:
    cursor.execute(statement)
conn.commit()

json_files = [
    'cleaned_Airtime.json',
    'cleaned_Bundles.json',
    'cleaned_cash_power.json',
    'cleaned_deposit.json',
    'cleaned_incoming_money.json',
    'cleaned_payments.json',
    'cleaned_failed.json',
    'cleaned_reversed.json',
    'cleaned_third_party.json',
    'cleaned_transfer.json',
    'cleaned_withdraw.json',
    'cleaned_rest.json'
]

