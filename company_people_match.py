import requests
import pandas as pd
from time import sleep

api_key = "xjkthYXAtl1uuN4AtJ2HDA"
search_url = "https://api.apollo.io/v1/mixed_people/search"
email_unlock_url = "https://api.apollo.io/v1/people/match"

headers = {
    "Content-Type": "application/json",
    "Cache-Control": "no-cache"
}


df_companies = pd.read_csv('companyextract.csv')
company_names = df_companies['A'].dropna().tolist()[1:]  


search_data = {
    "api_key": api_key,
    "person_locations": ["Nigeria"],
    "organization_locations": ["Nigeria"],
    "titles": ["CEO", "Founder", "CEO and Founder", "Founder and CEO", "CFO", "CTO", "Co-Founder"],
    "organization_titles": ["Chief Executive Officer", "Chief Financial Officer", "Chief Technology Officer"],
    "page": 1,
    "per_page": 100
}

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

def extract_person_info(person):
    person_id = person.get('id')
    email = unlock_email(person_id) if person_id else 'N/A'
    
    return {
        "Name": person.get('name', 'N/A'),
        "Email": email,
        "Company": person.get('organization', {}).get('name', 'N/A'),
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

for company in company_names:
    if people_count >= 10:
        break
    
    print(f"Searching for people in company: {company}")
    page = 1
    company_results = fetch_data(page, company)
    
    if company_results:
        people = company_results.get('people', [])
        for person in people:
            if people_count >= 10:
                break
            person_info = extract_person_info(person)
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