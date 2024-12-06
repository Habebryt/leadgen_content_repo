import pandas as pd
import random
import re

def clean_and_split_keywords(keywords):
    """
    Clean and split keywords, handling various delimiter scenarios.
    
    Args:
        keywords (str): Raw keyword string
    
    Returns:
        list: Cleaned and processed keywords
    """
    if pd.isna(keywords):
        return []
    
    # Split by common delimiters and clean
    keywords_list = re.split(r'[,;|/&]', str(keywords))
    
    # Remove extra whitespace and filter out empty strings
    return [kw.strip() for kw in keywords_list if kw.strip()]

def generate_reason(row):
    """
    Generate a reason based on keywords, SEO Description, and Technologies.
    
    Args:
        row (pd.Series): A row from the DataFrame
    
    Returns:
        str: A generated reason that contextualizes the input data
    """
    # Clean and split inputs
    keywords = clean_and_split_keywords(row['Keywords'])
    technologies = clean_and_split_keywords(row['Technologies'])
    
    # Fallback if no inputs
    if not keywords and not technologies:
        return "Providing innovative solutions tailored to unique business needs."
    
    # Reason templates
    reason_templates = [
        "Specializing in {keywords} through {tech} to {benefit}.",
        "Leveraging {tech} for comprehensive {keywords} strategies.",
        "Expert {keywords} solutions powered by advanced {tech}.",
        "Driving {benefit} with our {keywords} and {tech} expertise."
    ]
    
    # Benefits and selection logic
    benefits = [
        "business growth", "digital transformation", 
        "operational efficiency", "market optimization"
    ]
    
    # Select inputs
    tech = technologies[0] if technologies else "innovative technologies"
    keyword_str = " and ".join(keywords[:3]) if keywords else "cutting-edge solutions"
    benefit = random.choice(benefits)
    
    # Generate reason
    reason = random.choice(reason_templates).format(
        keywords=keyword_str, 
        tech=tech, 
        benefit=benefit
    )
    
    return reason

def process_csv(input_file, output_file):
    """
    Process the input CSV file and generate reasons.
    
    Args:
        input_file (str): Path to the input CSV file
        output_file (str): Path to save the updated CSV file
    """
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Add reason column
    df['Reason'] = df.apply(generate_reason, axis=1)
    
    # Save updated CSV
    df.to_csv(output_file, index=False)
    
    print(f"Updated CSV saved to {output_file}")

# Example usage
if __name__ == "__main__":
    input_file = "accounts.csv"
    output_file = "account_updated.csv"
    
    process_csv(input_file, output_file)