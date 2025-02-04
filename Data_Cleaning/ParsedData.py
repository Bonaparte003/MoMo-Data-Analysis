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




#Process SMS messages
total_sms = 0
for sms in root.findall('.//sms'):
    body = sms.get('body', '').strip() #Ensure no missing or empty body
    if not body:
        continue #Skip SMS with no body

    total_sms += 1
    category = categorize_sms(body)
    categories_count[category] += 1

#Print results
print(f"Total SMS entries found: {total_sms}")
for category, count in categories_count.items():
    print(f"{category}: {count} transactions")