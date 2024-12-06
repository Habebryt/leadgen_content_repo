import requests
import pandas as pd
from time import sleep
import os

# Install fuzzywuzzy !pip install fuzzywuzzy
from fuzzywuzzy import fuzz
import re

api_key = "Your Apollo API Key" #Input your apollo master API Key
search_url = "https://api.apollo.io/v1/mixed_people/search"
email_unlock_url = "https://api.apollo.io/v1/people/match"

headers = {
    "Content-Type": "application/json",
    "Cache-Control": "no-cache"
}

def get_csv_file():
    while True:
        file_name = input("Enter the name of your CSV file (including .csv extension): ")
        if os.path.exists(file_name):
            return file_name
        else:
            print(f"File '{file_name}' not found. Please make sure the file is in the same directory as this script.")

csv_file = get_csv_file()

try:
    df_companies = pd.read_csv(csv_file)
    company_names = df_companies.iloc[:, 0].dropna().tolist()[1:]
except Exception as e:
    print(f"Error reading the CSV file: {e}")
    print("Please make sure the file is a valid CSV and contains company names in the first column.")
    exit(1)

search_data = {
    "api_key": api_key,
    "person_locations": ["Nigeria"],
    "organization_locations": ["Nigeria"],
    "titles": ["CEO", "Founder", "CEO and Founder", "Founder and CEO", "CFO", "CTO", "Co-Founder"],
    "organization_titles": ["Chief Executive Officer", "Chief Financial Officer", "Chief Technology Officer"],
    "page": 1,
    "per_page": 100
}

def clean_company_name(name):
    # Remove common suffixes and clean the name
    suffixes = r'\b(Limited|Ltd|LLC|Inc|Corporation|Corp|Company|Co)\b'
    cleaned = re.sub(suffixes, '', name, flags=re.IGNORECASE).strip()
    return re.sub(r'[^\w\s]', '', cleaned).lower()

def fetch_data(page, company_name):
    search_data["page"] = page
    search_data["q_organization_domains"] = company_name
    response = requests.post(search_url, json=search_data, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error on page {page} for company {company_name}: {response.status_code}")
        print(response.text)
        return None

def unlock_email(person_id):
    unlock_data = {
        "api_key": api_key,
        "id": person_id
    }
    response = requests.post(email_unlock_url, json=unlock_data, headers=headers)
    
    if response.status_code == 200:
        return response.json().get('person', {}).get('email', 'N/A')
    else:
        print(f"Error unlocking email for person {person_id}: {response.status_code}")
        print(response.text)
        return 'N/A'

def extract_person_info(person, original_company_name):
    person_id = person.get('id')
    email = unlock_email(person_id) if person_id else 'N/A'
    
    return {
        "Name": person.get('name', 'N/A'),
        "Email": email,
        "Original Company": original_company_name,
        "Matched Company": person.get('organization', {}).get('name', 'N/A'),
        "Title": person.get('title', 'N/A'),
        "LinkedIn": person.get('linkedin_url', 'N/A'),
        "City": person.get('city', 'N/A'),
        "State": person.get('state', 'N/A'),
        "Country": person.get('country', 'N/A'),
        "Company City": person.get('organization', {}).get('city', 'N/A'),
        "Company State": person.get('organization', {}).get('state', 'N/A'),
        "Company Country": person.get('organization', {}).get('country', 'N/A')
    }

all_people = []
people_count = 0

for original_company in company_names:
    if people_count >= 10:
        break
    
    print(f"Searching for people in company: {original_company}")
    page = 1
    company_results = fetch_data(page, original_company)
    
    if company_results:
        people = company_results.get('people', [])
        if not people:
           
            # If no exact match, try fuzzy matching 
            cleaned_original = clean_company_name(original_company)
            for person in company_results.get('people', []):
                apollo_company = person.get('organization', {}).get('name', '')
                cleaned_apollo = clean_company_name(apollo_company)
                if fuzz.ratio(cleaned_original, cleaned_apollo) > 80:  # Adjust threshold as needed
                    person_info = extract_person_info(person, original_company)
                    if person_info["Email"] != 'N/A':
                        all_people.append(person_info)
                        people_count += 1
                        print(f"Added (Fuzzy Match): {person_info['Name']} - {person_info['Email']}")
                        print(f"Original: {original_company}, Matched: {apollo_company}")
                        break
        else:
            for person in people:
                if people_count >= 10:
                    break
                person_info = extract_person_info(person, original_company)
                if person_info["Email"] != 'N/A':
                    all_people.append(person_info)
                    people_count += 1
                    print(f"Added: {person_info['Name']} - {person_info['Email']}")
    
    sleep(1)  

df = pd.DataFrame(all_people)
csv_filename = "nigeria_executives_and_companies_sample_with_unlocked_emails.csv"
df.to_csv(csv_filename, index=False)
print(f"Data saved to {csv_filename}")
print(f"Total records fetched: {len(all_people)}")

print("\nNames and Emails:")
for person in all_people:
    print(f"{person['Name']} - {person['Email']}")
    print(f"Original Company: {person['Original Company']}")
    print(f"Matched Company: {person['Matched Company']}")
    print("---")