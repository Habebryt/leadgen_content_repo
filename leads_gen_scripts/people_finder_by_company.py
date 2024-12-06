import requests
import pandas as pd
from time import sleep

api_key = "Your Apollo Master API Key"
url = "https://api.apollo.io/v1/mixed_people/search"

headers = {
    "Content-Type": "application/json",
    "Cache-Control": "no-cache"
}

# Updated search parameters
data = {
    "api_key": api_key,
    "person_locations": ["Nigeria"],  # People located in country of your choice
    "organization_locations": ["Nigeria"],  # Companies located in your country of choice or location
    "titles": ["CEO", "Founder", "CEO and Founder", "Founder and CEO", "CFO", "CTO", "Co-Founder"], #Fdesired job titles.
    "organization_titles": ["Chief Executive Officer", "Chief Financial Officer", "Chief Technology Officer"],
    "page": 1,
    "per_page": 100  # Maximum allowed by Apollo
}

def fetch_data(page):
    data["page"] = page
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error on page {page}: {response.status_code}")
        print(response.text)
        return None

def extract_person_info(person):
    return {
        "Name": person.get('name', 'N/A'),
        "Email": person.get('email', 'N/A'),
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
page = 1
total_pages = 1

while page <= total_pages:
    print(f"Fetching page {page}...")
    results = fetch_data(page)
    
    if results:
        people = results.get('people', [])
        all_people.extend([extract_person_info(person) for person in people])
        
        total_pages = results.get('pagination', {}).get('total_pages', 1)
        page += 1
        
        if page <= total_pages:
            sleep(1)  # Respect rate limits
    else:
        break

df = pd.DataFrame(all_people)
csv_filename = "nigeria_executives_and_companies.csv" #CSV file export
df.to_csv(csv_filename, index=False)
print(f"Data saved to {csv_filename}")
print(f"Total records fetched: {len(all_people)}")