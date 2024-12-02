import pandas as pd

# Load files
accounts_path = 'apollo-accounts-export.csv'  
contacts_path = 'apollo-contacts-export.csv'

# Load the data
accounts_data = pd.read_csv(accounts_path)
contacts_data = pd.read_csv(contacts_path)

# Display the first few rows of each file
print("Accounts Data:")
print(accounts_data.head())

print("\nContacts Data:")
print(contacts_data.head())
