import pandas as pd
from openai import OpenAI

# Directly put your API key here
client = OpenAI(api_key='OPENAI API KEY')

def generate_reason_with_ai(row):
    keywords = str(row['Keywords'])
    seo_description = str(row['SEO Description'])
    technologies = str(row['Technologies'])
    
    prompt = f"""Generate a professional, coherent business reason that incorporates these details:
    Keywords: {keywords}
    SEO Description: {seo_description}
    Technologies: {technologies}
    
    Reason should be 1-2 sentences, sound natural, and highlight business value."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional business content generator."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Reason generation failed: {e}"

def process_csv(input_file, output_file):
    df = pd.read_csv(input_file)
    df['Reason'] = df.apply(generate_reason_with_ai, axis=1)
    df.to_csv(output_file, index=False)
    print(f"Updated CSV saved to {output_file}")

# Usage
if __name__ == "__main__":
    input_file = "accounts.csv" #Name of your CSV File
    output_file = "1account_updated.csv" #Name of your Output CSV File
    process_csv(input_file, output_file)