import sqlite3
import json
import os

DB_FILE = "momo_transactions.db"

# Dictionary mapping table names to JSON files
json_files = {
    "Airtime": "Data_Categorization/Cleaned_Data/cleaned_Airtime.json",
    "Bundles": "Data_Categorization/Cleaned_Data/cleaned_Bundles.json",
    "Cash_Power": "Data_Categorization/Cleaned_Data/cleaned_cash_power.json",
    "Deposit": "Data_Categorization/Cleaned_Data/cleaned_deposit.json",
    "Incoming_Money": "Data_Categorization/Cleaned_Data/cleaned_incoming_money.json",
    "Payments": "Data_Categorization/Cleaned_Data/cleaned_payments.json",
    "Failed_Transactions": "Data_Categorization/Cleaned_Data/cleaned_failed.json",
    "Reversed_Transactions": "Data_Categorization/Cleaned_Data/cleaned_reversed.json",
    "Third_Party": "Data_Categorization/Cleaned_Data/cleaned_third_party.json",
    "Transfer": "Data_Categorization/Cleaned_Data/cleaned_transfer.json",
    "Withdraw": "Data_Categorization/Cleaned_Data/cleaned_withdraw.json"
}

def connect_db():
    try:
        conn = sqlite3.connect(DB_FILE)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_table(conn, table_name, sample_data):
    """Create a table with columns based on the sample data."""
    try:
        cursor = conn.cursor()
        columns = ", ".join([f"{key} TEXT" for key in sample_data.keys()])
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        cursor.execute(sql)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error creating table {table_name}: {e}")

def insert_data(conn, table, data):
    """Insert data into the specified table in SQLite."""
    try:
        cursor = conn.cursor()
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        sql = f"INSERT OR IGNORE INTO {table} ({columns}) VALUES ({placeholders})"
        cursor.execute(sql, tuple(data.values()))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error inserting into {table}: {e}")

def process_json_files(conn):
    """Read and insert data from JSON files into corresponding tables."""
    for table, file_path in json_files.items():
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}, skipping {table}")
            continue
        
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data_list = json.load(file)
                if isinstance(data_list, list) and data_list:
                    create_table(conn, table, data_list[0])
                    for data in data_list:
                        insert_data(conn, table, data)
                else:
                    print(f"Invalid or empty JSON format in {file_path}")
            
            print(f"Inserted data from {file_path} into {table} successfully.")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

def main():
    conn = connect_db()
    if conn:
        process_json_files(conn)
        conn.close()
        print("Data insertion complete and connection closed.")
    else:
        print("Database connection failed. Exiting.")

if __name__ == "__main__":
    main()