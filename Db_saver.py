import MySQLdb
import json
from dotenv import load_dotenv
import os
import datetime
import re

load_dotenv()

conn = MySQLdb.connect(
    host=os.getenv('MYSQL_HOST'),
    user=os.getenv('MYSQL_USER'),
    passwd=os.getenv('MYSQL_PASSWD'),
    db=os.getenv('DB')
)
cursor = conn.cursor()

sqlstatements = [
    """CREATE TABLE IF NOT EXISTS airtime (
    TxId VARCHAR(250) PRIMARY KEY NOT NULL,
    Amount INT, 
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME, 
    Type VARCHAR(250), 
    Balance INT, 
    Fee INT
    );""",
    
    """CREATE TABLE IF NOT EXISTS bundles(
    TxId VARCHAR(250) PRIMARY KEY NOT NULL,
    Amount INT,
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME,
    Type VARCHAR(250),
    Balance INT,
    Fee INT
    );
    """,
    
    """CREATE TABLE IF NOT EXISTS cashpower(
    TxId VARCHAR(250) PRIMARY KEY NOT NULL,
    TOKEN VARCHAR(250),
    Amount INT,
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME,
    Type VARCHAR(250),
    Balance INT,
    Fee INT
    );""",
    
    """CREATE TABLE IF NOT EXISTS deposit(
    AMOUNT INT,
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME,
    Type VARCHAR(250),
    Balance INT,
    Fee INT
    );""",
    
    """CREATE TABLE IF NOT EXISTS incomingmoney(
    SENDER VARCHAR(250),
    AMOUNT INT,
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME,
    Type VARCHAR(250),
    Balance INT,
    Fee INT
    );""",
    
    """CREATE TABLE IF NOT EXISTS payments(
    TxId VARCHAR(250) PRIMARY KEY NOT NULL,
    RECEIVER VARCHAR(250),
    PHONE_NUMBER VARCHAR(250),
    AMOUNT INT,
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME,
    Type VARCHAR(250),
    Balance INT,
    Fee INT
    );""",
    
    """CREATE TABLE IF NOT EXISTS failedtransactions(
    TxId VARCHAR(250) PRIMARY KEY NOT NULL,
    RECEIVER VARCHAR(250),
    AMOUNT INT,
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME,
    Type TEXT
    );""",
    
    """CREATE TABLE IF NOT EXISTS reversedtransactions(
    RECEIVER VARCHAR(250),
    AMOUNT INT,
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME,
    Type VARCHAR(250),
    BALANCE INT
    );""",
    
    """CREATE TABLE IF NOT EXISTS thirdparty(
    TxId VARCHAR(250) PRIMARY KEY NOT NULL,
    SENDER VARCHAR(250),
    AMOUNT INT,
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME,
    Type VARCHAR(250),
    Balance INT,
    Fee INT
    );""",
    
    """CREATE TABLE IF NOT EXISTS transfer(
    RECEIVER VARCHAR(250),
    PHONE_NUMBER VARCHAR(250),
    AMOUNT INT,
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME,
    Type VARCHAR(250),
    Balance INT,
    Fee INT
    );""",
    
    """CREATE TABLE IF NOT EXISTS withdraw(
    AGENT VARCHAR(250),
    AMOUNT INT,
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME,
    Type VARCHAR(250),
    Balance INT,
    Fee INT
    );""",
    
    """CREATE TABLE IF NOT EXISTS nontransaction(
    NUMBER INT);"""
]

for statement in sqlstatements:
    cursor.execute(statement)
conn.commit()

json_files = [
    'Data_Categorization/Cleaned_Data/cleaned_Airtime.json',
    'Data_Categorization/Cleaned_Data/cleaned_Bundles.json',
    'Data_Categorization/Cleaned_Data/cleaned_cash_power.json',
    'Data_Categorization/Cleaned_Data/cleaned_deposit.json',
    'Data_Categorization/Cleaned_Data/cleaned_incoming_money.json',
    'Data_Categorization/Cleaned_Data/cleaned_payments.json',
    'Data_Categorization/Cleaned_Data/cleaned_failed.json',
    'Data_Categorization/Cleaned_Data/cleaned_reversed.json',
    'Data_Categorization/Cleaned_Data/cleaned_third_party.json',
    'Data_Categorization/Cleaned_Data/cleaned_transfer.json',
    'Data_Categorization/Cleaned_Data/cleaned_withdraw.json',
    'Data_Categorization/Cleaned_Data/cleaned_Non_transaction.json'
]

column_mappings = {
    "airtime": {
        "TransactionId": "TxId",
        "amount": "Amount",
        "currency": "CURRENCY",
        "Date": "Date",
        "Time": "TIME",
        "transaction_type": "Type",
        "current_balance": "Balance",
        "fee": "Fee"
    },
    "bundles": {
        "TransactionId": "TxId",
        "amount": "Amount",
        "currency": "CURRENCY",
        "Date": "Date",
        "Time": "TIME",
        "transaction_type": "Type",
        "current_balance": "Balance",
        "fee": "Fee"
    },
    "cashpower": {
        "TransactionId": "TxId",
        "token": "TOKEN",
        "amount": "Amount",
        "currency": "CURRENCY",
        "Date": "Date",
        "Time": "TIME",
        "transaction_type": "Type",
        "current_balance": "Balance",
        "fee": "Fee"
    },
    "payments": {
        "TransactionId": "TxId",
        "amount": "AMOUNT",
        "currency": "CURRENCY",
        "Date": "Date",
        "Time": "TIME",
        "transaction_type": "Type",
        "current_balance": "Balance",
        "fee": "Fee"
    },
    "failedtransactions": {
        "TransactionId": "TxId",
        "ReceiverName": "RECEIVER",
        "AmountPaid": "AMOUNT",
        "Currency": "CURRENCY",
        "Date": "Date",
        "Time": "TIME",
        "TransactionType": "Type"
    },
    "reversedtransactions": {
        "receiver": "RECEIVER",
        "amount": "AMOUNT",
        "currency": "CURRENCY",
        "Date": "Date",
        "Time": "TIME",
        "transaction_type": "Type",
        "current_balance": "BALANCE"
    },
    "thirdparty": {
        "third_party_sender": "SENDER",
        "amount": "AMOUNT",
        "currency": "CURRENCY",
        "Date": "Date",
        "Time": "TIME",
        "transaction_type": "Type",
        "current_balance": "Balance",
        "fee": "Fee"
    },
    "withdraw": {
        "agent": "AGENT",
        "amount": "AMOUNT",
        "currency": "CURRENCY",
        "Date": "Date",
        "Time": "TIME",
        "transaction_type": "Type",
        "current_balance": "Balance",
        "fee": "Fee"
    },
    "nontransaction": {
        "number": "NUMBER"
    },
    "incomingmoney": {
        "sender": "SENDER",
        "amount": "AMOUNT",
        "currency": "CURRENCY",
        "Date": "Date",
        "Time": "TIME",
        "transaction_type": "Type",
        "current_balance": "Balance",
        "fee": "Fee"
    },
    "transfer": {
        "receiver": "RECEIVER",
        "phone_number": "PHONE_NUMBER",
        "amount": "AMOUNT",
        "currency": "CURRENCY",
        "Date": "Date",
        "Time": "TIME",
        "transaction_type": "Type",
        "current_balance": "Balance",
        "fee": "Fee"
    },
    "deposit": {
        "amount": "AMOUNT",
        "currency": "CURRENCY",
        "Date": "Date",
        "Time": "TIME",
        "transaction_type": "Type",
        "current_balance": "Balance",
        "fee": "Fee"
    }
}

def normalize_table_name(file_name):
    return re.sub(r'[^a-zA-Z0-9]', '', file_name.lower())

for file in json_files:
    print(file)
    table_name = normalize_table_name(file.split('/')[-1].split('_')[1].split('.')[0])

    if file == 'Data_Categorization/Cleaned_Data/cleaned_Non_transaction.json':
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            number_of_objects = len(data)
            cursor.execute("INSERT INTO nontransaction (NUMBER) VALUES (%s)", (number_of_objects,))
    else:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if table_name in column_mappings:
                # Filter out entries with 'Unknown' date
                data = [i for i in data if i.get('Date') != 'Unknown']
                # Sort data by Date in descending order
                data.sort(key=lambda x: datetime.datetime.strptime(x['Date'], '%Y-%m-%d'), reverse=True)
                for i in data:
                    if 'Unknown' in i.values():
                        continue
                    
                    # Convert date and time formats if present
                    if i.get('Date'):
                        i['Date'] = datetime.datetime.strptime(i['Date'].replace('/', '-'), '%Y-%m-%d').date()
                    if i.get('Time'):
                        i['Time'] = datetime.datetime.strptime(i['Time'], '%H:%M:%S').time()
                    
                    # Map JSON keys to table column names
                    mapped_data = {column_mappings[table_name][key]: value for key, value in i.items() if key in column_mappings[table_name]}
                    
                    # Create SQL statement dynamically
                    columns = ', '.join(mapped_data.keys())
                    placeholders = ', '.join(['%s'] * len(mapped_data))
                    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                    
                    cursor.execute(sql, list(mapped_data.values()))

conn.commit()
cursor.close()
conn.close()