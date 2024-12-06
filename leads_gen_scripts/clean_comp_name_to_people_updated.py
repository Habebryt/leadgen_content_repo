import requests
import pandas as pd
from time import sleep
import os
from fuzzywuzzy import fuzz
import re
import chardet

# API configuration
api_key = "Your Apollo API Key" #Input your apollo master API Key
search_url = "https://api.apollo.io/v1/mixed_people/search"
email_unlock_url = "https://api.apollo.io/v1/people/match"

headers = {
    "Content-Type": "application/json",
    "Cache-Control": "no-cache"
}

# Updated Priority order of titles with HR roles
PRIORITY_TITLES = [
    # HR/Recruitment Group
    ["HR Manager", "Human Resources Manager", "HR Director", "Human Resources Director", 
     "Head of HR", "Human Resources Head", "HR Business Partner", "HRBP",
     "Talent Acquisition Manager", "Talent Acquisition Specialist", "Recruitment Manager",
     "Talent Manager", "HR Specialist", "Human Resources Specialist",
     "Talent Acquisition Lead", "Recruiting Manager", "Technical Recruiter"],
    
    # Executive Group
    ["CEO", "Chief Executive Officer", "Managing Director"],
    ["Founder", "Co-Founder"],
    ["CFO", "Chief Financial Officer", "Finance Director"],
    ["CTO", "Chief Technology Officer", "Technical Director"],
    ["COO", "Chief Operating Officer", "Operations Director"],
    
    # Additional HR Titles
    ["HR Coordinator", "Human Resources Coordinator", "HR Assistant",
     "Recruitment Coordinator", "Talent Coordinator", "Recruitment Specialist",
     "HR Administrator", "Human Resources Administrator"]
]

def detect_file_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    result = chardet.detect(raw_data)
    return result['encoding']

def read_csv_with_encoding(file_path):
    detected_encoding = detect_file_encoding(file_path)
    encodings = [detected_encoding, 'utf-8', 'utf-8-sig', 'iso-8859-1', 'cp1252', 'latin1']
    
    for encoding in encodings:
        try:
            print(f"Trying to read file with {encoding} encoding...")
            df = pd.read_csv(file_path, encoding=encoding)
            if not df.empty and len(df.columns) > 0:
                first_col = df.columns[0]
                companies = df[first_col].dropna().tolist()
                print(f"\nFirst few company names found:")
                for company in companies[:5]:
                    print(f"- {company}")
                return df
        except Exception as e:
            print(f"Failed with {encoding} encoding: {str(e)}")
            continue
    
    raise ValueError("Unable to read the CSV file with any supported encoding")

def clean_company_name(name):
    suffixes = r'\b(Limited|Ltd|LLC|Inc|Corporation|Corp|Company|Co)\b'
    cleaned = re.sub(suffixes, '', str(name), flags=re.IGNORECASE).strip()
    return re.sub(r'[^\w\s]', '', cleaned).lower()

def check_title_priority(title):
    """Check if a title matches our priority list and return its priority level"""
    if not title:
        return -1
    
    title = title.lower()
    for i, title_group in enumerate(PRIORITY_TITLES):
        if any(t.lower() in title for t in title_group):
            return i
    return len(PRIORITY_TITLES)

def fetch_data(page, company_name):
    # Flatten the PRIORITY_TITLES list for the API call
    all_titles = [title for sublist in PRIORITY_TITLES for title in sublist]
    
    search_data = {
        "api_key": api_key,
        "person_locations": ["Nigeria"],
        "organization_locations": ["Nigeria"],
        "titles": all_titles,
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
        "Country": person.get('country', 'N/A')
    }

def main():
    try:
        csv_file = input("Enter the name of your CSV file (including .csv extension): ")
        df_companies = read_csv_with_encoding(csv_file)
        first_col = df_companies.columns[0]
        company_names = df_companies[first_col].dropna().tolist()
        company_names = [name for name in company_names if isinstance(name, str)]
        
        print(f"\nFound {len(company_names)} companies to process")
        
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return

    all_people = []
    timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    
    for i, original_company in enumerate(company_names, 1):
        print(f"\nProcessing company {i}/{len(company_names)}: {original_company}")
        
        company_people = []
        page = 1
        all_candidates = []
        
        # Fetch all potential candidates
        while True:
            print(f"Fetching page {page}...")
            results = fetch_data(page, original_company)
            
            if not results or not results.get('people'):
                break
                
            people = results.get('people', [])
            all_candidates.extend(people)
            
            total_pages = results.get('pagination', {}).get('total_pages', 1)
            if page >= total_pages:
                break
                
            page += 1
            sleep(1)
        
        # Sort candidates by title priority and company name match
        cleaned_original = clean_company_name(original_company)
        prioritized_candidates = []
        
        for person in all_candidates:
            apollo_company = person.get('organization', {}).get('name', '')
            cleaned_apollo = clean_company_name(apollo_company)
            
            # Calculate match scores
            title_priority = check_title_priority(person.get('title', ''))
            company_match_score = fuzz.ratio(cleaned_original, cleaned_apollo)
            
            prioritized_candidates.append((person, title_priority, company_match_score))
        
        # Sort by title priority (higher priority = lower number) and company match score
        prioritized_candidates.sort(key=lambda x: (x[1], -x[2]))
        
        # Process candidates by group to ensure one HR person
        hr_found = False
        total_added = 0
        
        for person, priority, _ in prioritized_candidates:
            if total_added >= 5:  # Maximum 5 people per company
                break
                
            person_info = extract_person_info(person, original_company)
            
            # Skip if email is invalid
            if person_info["Email"] == 'N/A':
                continue
                
            # Check if this is an HR role
            is_hr_role = priority == 0  # First group in PRIORITY_TITLES is HR roles
            
            # Add HR person if we haven't found one yet
            if is_hr_role and not hr_found:
                company_people.append(person_info)
                hr_found = True
                total_added += 1
                print(f"Added HR Contact: {person_info['Name']} - {person_info['Title']} - {person_info['Email']}")
            # Add other roles up to the limit
            elif not is_hr_role and total_added < 5:
                company_people.append(person_info)
                total_added += 1
                print(f"Added: {person_info['Name']} - {person_info['Title']} - {person_info['Email']}")
        
        all_people.extend(company_people)
        print(f"Found {len(company_people)} people for {original_company}")
        
        # Save intermediate results
        if all_people:
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