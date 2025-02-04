import xml.etree.ElementTree as ET
import re

# Load the XML file (Replace with your actual XML file path)
tree = ET.parse(r'C:\users\lenovo\MoMo-Data-Analysis\Data_Cleaning\modified_sms_v2.xml')  
root = tree.getroot()

# Dictionary to store categorized SMS details
categories_data = {
    'Incoming Money': [],
    'Payments to Code Holders': [],
    'Transfers to Mobile Numbers': [],
    'Bank Deposits': [],
    'Airtime Bill Payments': [],
    'Cash Power Bill Payments': [],
    'Transactions Initiated by Third Parties': [],
    'Withdrawals from Agents': [],
    'Bank Transfers': [],
    'Internet and Voice Bundle Purchases': [],
    'Other': []
}

# Function to categorize SMS based on keywords
def categorize_sms(body):
    body = body.lower()
    if 'received' in body or 'credited' in body:
        return 'Incoming Money'
    elif 'payment' in body or 'code holder' in body:
        return 'Payments to Code Holders'
    elif 'deposit' in body:
        return 'Bank Deposits'
    elif 'transferred to' in body or 'sent to' in body:
        return 'Transfers to Mobile Numbers'
    elif 'withdraw' in body:
        return 'Withdrawals from Agents'
    elif 'airtime' in body or 'top-up' in body:
        return 'Airtime Bill Payments'
    elif 'cash power' in body or 'electricity' in body:
        return 'Cash Power Bill Payments'
    elif 'third party' in body:
        return 'Transactions Initiated by Third Parties'
    elif 'bank transfer' in body:
        return 'Bank Transfers'
    elif 'bundle' in body or 'internet' in body or 'voice' in body:
        return 'Internet and Voice Bundle Purchases'
    else:
        return 'Other' 

# Function to extract transaction details from SMS body
def extract_transaction_details(body):
    details = {}

    # Extract Transaction ID
    tx_id_match = re.search(r'(TxId|Transaction ID|Financial Transaction Id)[:\s]+(\w+)', body, re.IGNORECASE)
    details['Transaction ID'] = tx_id_match.group(2) if tx_id_match else "UNKNOWN"

    # Extract Date and Time
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})', body)
    if date_match:
        details['Date'] = date_match.group(1)
        details['Time'] = date_match.group(2)

    # Extract Sender Name
    sender_match = re.search(r'from\s+([\w\s]+?)(?:\s*\(|$)', body, re.IGNORECASE)
    details['Sender'] = sender_match.group(1).strip() if sender_match else "UNKNOWN"

    # Extract Amount
    amount_match = re.search(r'(\d{1,3}(?:,\d{3})*|\d+)\s?(RWF|Rwf|rwf)', body)
    details['Amount'] = amount_match.group(1) + " RWF" if amount_match else "0 RWF"

    # Extract Transaction Fee (optional, only add if found)
    fee_match = re.search(r'Fee\s*was\s*(\d+)\s?RWF', body, re.IGNORECASE)
    if fee_match:
        details['Transaction Fee'] = fee_match.group(1) + " RWF"

    return details

# Process SMS messages in order
sms_list = []  # Stores SMS in order of appearance

for sms in root.findall('.//sms'):   
    body = sms.get('body', '').strip()  
    if not body:
        continue  

    category = categorize_sms(body)
    transaction_details = extract_transaction_details(body)
    
    # Append transaction details in order to the list
    sms_list.append((category, transaction_details))

# Sort SMS messages based on their appearance in the XML (already in order)
for category, transaction in sms_list:
    categories_data[category].append(transaction)

# Calculate total transactions and money spent per category
total_sms = len(sms_list)
category_totals = {}

for category, transactions in categories_data.items():
    total_amount = 0
    for txn in transactions:
        # Extract numeric value of Amount
        amount_value = int(txn['Amount'].replace(" RWF", "").replace(",", ""))
        total_amount += amount_value
    
    category_totals[category] = total_amount

# Process SMS messages in order
sms_list = []  # Stores SMS in order of appearance

for sms in root.findall('.//sms'):   
    body = sms.get('body', '').strip()  
    if not body:
        continue  

    category = categorize_sms(body)
    transaction_details = extract_transaction_details(body)
    
    # Append transaction details in order to the list
    sms_list.append((category, transaction_details))

# Sort SMS messages based on their appearance in the XML (already in order)
for category, transaction in sms_list:
    categories_data[category].append(transaction)

# Sort SMS messages based on their appearance in the XML (already in order)
for category, transaction in sms_list:
    categories_data[category].append(transaction)

# Calculate total transactions and money spent per category
total_sms = len(sms_list)
category_totals = {}

for category, transactions in categories_data.items():
    total_amount = 0
    for txn in transactions:
        # Extract numeric value of Amount
        amount_value = int(txn['Amount'].replace(" RWF", "").replace(",", ""))
        total_amount += amount_value
    
    category_totals[category] = total_amount


# Save to file to avoid terminal cutoff
output_file = r'C:\users\lenovo\MoMo-Data-Analysis\Data_Cleaning\transaction_report.txt'

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(f"\nTotal SMS entries found: {total_sms}\n\n")

    for category, transactions in categories_data.items():
        count = len(transactions)
        total_spent = category_totals[category]
        
        f.write(f"=== {category} ({count} transactions) ===\n")
        f.write(f"Total Amount Spent: {total_spent} RWF\n\n")

        if count == 0:
            f.write("  No transactions found.\n\n")
        else:
            for i, txn in enumerate(transactions, start=1):
                f.write(f"  Transaction {i}:\n")
                for key, value in txn.items():
                    if key == "Transaction Fee":
                        f.write(f"    {key}: {value}\n")  # Print only if it exists
                    elif key == "Transaction ID" and value == "UNKNOWN":
                        f.write(f"    {key}: ERROR - Missing ID\n")  # Warn about missing ID
                    else:
                        f.write(f"    {key}: {value}\n")
                f.write("\n")
        
        f.write("\n" + "="*50 + "\n\n")  # Separator for readability

print(f"✅ Transaction report saved to: {output_file}")