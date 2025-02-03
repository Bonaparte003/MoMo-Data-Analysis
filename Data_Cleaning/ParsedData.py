import xml.etree.ElementTree as ET

#Load the XML file
try:
    tree = ET.parse(r'C:\users\lenovo\MoMo-Data-Analysis\data-cleaning\modified_sms_v2.xml')
    root = tree.getroot()
except ET.ParseError as e:
    print(f"Error parsing XML file: {e}")
    exit()
except FileNotFoundError:
    print("XML file not found.")
    exit()

#Dictionary to store transaction counts
categories_count = {
    'Incoming Money': 0,
    'Payments to Code Holders': 0,
    'Transfers to Mobile Numbers': 0,
    'Bank Deposits': 0,
    'Airtime Bill Payments': 0,
    'Cash Power Bill Payments': 0,
    'Transactions Initiated by Third Parties': 0,
    'Withdrawals from Agents': 0,
    'Bank Transfers': 0,
    'Internet and Voice Bundle Purchases': 0,
    'Other': 0
}

#Categorization function
def categorize_sms(body):
    body = body.lower().strip()
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
