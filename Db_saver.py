import sqlite3
import json
import os

def save_to_db(json_file_path, db_path):
    table_name = os.path.splitext(os.path.basename(json_file_path))[0]

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Read the JSON file
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Create table if it doesn't exist
    if data:
        columns = data[0].keys()
        columns_with_types = ", ".join([f"{col} TEXT" for col in columns])
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types})")

        # Insert data into the table
        for entry in data:
            placeholders = ", ".join(["?" for _ in entry])
            cursor.execute(f"INSERT INTO {table_name} ({', '.join(entry.keys())}) VALUES ({placeholders})", tuple(entry.values()))

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

# Example usage
json_files = [
    'cleaned_incoming_money.json',
    'cleaned_payments.json',
    'cleaned_deposit.json',
    'cleaned_withdraw.json',
    'cleaned_transfer.json',
    'cleaned_third_party.json',
    'cleaned_payment_code_holders.json',
    'cleaned_cash_power.json',
    'cleaned_Airtime.json',
    'cleaned_Bundles.json',
    'cleaned_rest.json'
]

db_path = 'data.db'

for json_file in json_files:
    json_file_path = os.path.join('Data_Categorization', 'Cleaned_Data', json_file)
    save_to_db(json_file_path, db_path)

print("Data has been saved to the database")