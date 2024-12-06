import pandas as pd
import google.generativeai as genai

# Configure your Google AI API key
genai.configure(api_key='Gemini Api Key') #Your Gemini Api key

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
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Reason generation failed: {e}"

def process_csv(input_file, output_file):
    df = pd.read_csv(input_file)
    df['Reason'] = df.apply(generate_reason_with_ai, axis=1)
    df.to_csv(output_file, index=False)
    print(f"Updated CSV saved to {output_file}")

# Usage
if __name__ == "__main__":
    input_file = "3contaccount_updated.csv"
    output_file = "6account_updated.csv"
    process_csv(input_file, output_file)