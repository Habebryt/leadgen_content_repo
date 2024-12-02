import requests
import pandas as pd
from time import sleep
import os
from fuzzywuzzy import fuzz
import re
import chardet

# API configuration
api_key = "xjkthYXAtl1uuN4AtJ2HDA"
search_url = "https://api.apollo.io/v1/mixed_people/search"
email_unlock_url = "https://api.apollo.io/v1/people/match"

headers = {
    "Content-Type": "application/json",
    "Cache-Control": "no-cache"
}

def detect_file_encoding(file_path):
    """Detect the encoding of a file using chardet"""
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    result = chardet.detect(raw_data)
    return result['encoding']

def get_csv_file():
    while True:
        file_name = input("Enter the name of your CSV file (including .csv extension): ")
        if os.path.exists(file_name):
            return file_name
        else:
            print(f"File '{file_name}' not found. Please make sure the file is in the same directory as this script.")

def read_csv_with_encoding(file_path):
    """Try multiple encodings to read the CSV file"""
    # First try to detect the encoding
    detected_encoding = detect_file_encoding(file_path)
    
    # List of encodings to try
    encodings = [
        detected_encoding,
        'utf-8',
        'utf-8-sig',
        'iso-8859-1',
        'cp1252',
        'latin1'
    ]
    
    for encoding in encodings:
        try:
            print(f"Trying to read file with {encoding} encoding...")
            df = pd.read_csv(file_path, encoding=encoding)
            print(f"Successfully read file with {encoding} encoding")
            
            # Verify the first column exists and has data
            if df.empty:
                print("File is empty")
                continue
                
            if len(df.columns) == 0:
                print("No columns found in file")
                continue
                
            # Get the first column name
            first_col = df.columns[0]
            print(f"First column name: {first_col}")
            
            # Show first few company names
            companies = df[first_col].dropna().tolist()
            print("\nFirst few company names found:")
            for company in companies[:5]:
                print(f"- {company}")
                
            return df
            
        except Exception as e:
            print(f"Failed with {encoding} encoding: {str(e)}")
            continue
    
    raise ValueError("Unable to read the CSV file with any supported encoding")

def clean_company_name(name):
    suffixes = r'\b(Limited|Ltd|LLC|Inc|Corporation|Corp|Company|Co)\b'
    cleaned = re.sub(suffixes, '', name, flags=re.IGNORECASE).strip()
    return re.sub(r'[^\w\s]', '', cleaned).lower()

def fetch_data(page, company_name):
    search_data = {
        "api_key": api_key,
        "person_locations": ["Nigeria"],
        "organization_locations": ["Nigeria"],
        "titles": ["CEO", "Founder", "CEO and Founder", "Founder and CEO", "CFO", "CTO", "Co-Founder"],
        "organization_titles": ["Chief Executive Officer", "Chief Financial Officer", "Chief Technology Officer"],
        "page": page,
        "per_page": 100,
        "q_organization_domains": company_name
    }
    
    try:
        response = requests.post(search_url, json=search_data, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error on page {page} for company {company_name}: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"Exception while fetching data: {e}")
        return None

def unlock_email(person_id):
    unlock_data = {
        "api_key": api_key,
        "id": person_id
    }
    try:
        response = requests.post(email_unlock_url, json=unlock_data, headers=headers)
        if response.status_code == 200:
            return response.json().get('person', {}).get('email', 'N/A')
        else:
            print(f"Error unlocking email for person {person_id}: {response.status_code}")
            return 'N/A'
    except Exception as e:
        print(f"Exception while unlocking email: {e}")
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

def main():
    csv_file = get_csv_file()
    
    try:
        # Use the new CSV reading function
        df_companies = read_csv_with_encoding(csv_file)
        first_col = df_companies.columns[0]
        company_names = df_companies[first_col].dropna().tolist()
        
        # Remove any header rows if present
        company_names = [name for name in company_names if isinstance(name, str) and not name.lower().startswith(('company', 'name', 'organisation', 'organization'))]
        
        print(f"\nFound {len(company_names)} companies to process")
        
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        print("Please check that your CSV file is properly formatted and contains company names in the first column.")
        return

    all_people = []
    timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    
    for i, original_company in enumerate(company_names, 1):
        print(f"\nProcessing company {i}/{len(company_names)}: {original_company}")
        page = 1
        company_people = []
        
        while True:
            print(f"Fetching page {page}...")
            company_results = fetch_data(page, original_company)
            
            if not company_results or not company_results.get('people'):
                break
                
            people = company_results.get('people', [])
            
            # Process exact matches first
            for person in people:
                apollo_company = person.get('organization', {}).get('name', '')
                if apollo_company.lower() == original_company.lower():
                    person_info = extract_person_info(person, original_company)
                    if person_info["Email"] != 'N/A':
                        company_people.append(person_info)
                        print(f"Added (Exact Match): {person_info['Name']} - {person_info['Email']}")
            
            # Then try fuzzy matching if no exact matches
            if not company_people:
                cleaned_original = clean_company_name(original_company)
                for person in people:
                    apollo_company = person.get('organization', {}).get('name', '')
                    cleaned_apollo = clean_company_name(apollo_company)
                    if fuzz.ratio(cleaned_original, cleaned_apollo) > 80:
                        person_info = extract_person_info(person, original_company)
                        if person_info["Email"] != 'N/A':
                            company_people.append(person_info)
                            print(f"Added (Fuzzy Match): {person_info['Name']} - {person_info['Email']}")
            
            # Check if we've processed all pages
            total_pages = company_results.get('pagination', {}).get('total_pages', 1)
            if page >= total_pages:
                break
                
            page += 1
            sleep(1)  # Rate limiting
        
        all_people.extend(company_people)
        print(f"Found {len(company_people)} people for {original_company}")
        
        # Save intermediate results after each company
        if all_people:  # Only save if we have data
            df = pd.DataFrame(all_people)
            intermediate_filename = f"nigeria_executives_{timestamp}_intermediate.xlsx"
            df.to_excel(intermediate_filename, index=False)
            print(f"Intermediate results saved to {intermediate_filename}")
    
    # Save final results
    if all_people:
        final_filename = f"nigeria_executives_{timestamp}_final.xlsx"
        df = pd.DataFrame(all_people)
        df.to_excel(final_filename, index=False)
        print(f"\nFinal data saved to {final_filename}")
        print(f"Total records fetched: {len(all_people)}")
        
        # Print summary
        print("\nSummary by Company:")
        company_summary = df.groupby('Original Company').agg({
            'Name': 'count',
            'Email': lambda x: (x != 'N/A').sum()
        }).rename(columns={'Name': 'Total People', 'Email': 'Valid Emails'})
        print(company_summary)
    else:
        print("\nNo data was collected. Please check the company names and try again.")

if __name__ == "__main__":
    main()