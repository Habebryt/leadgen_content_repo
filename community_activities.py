import pandas as pd
from datetime import datetime, timedelta

def generate_specific_calendar_excel():
    # Define the calendar data
    calendar_data = [
        # October 2024
        ("2024-10-22", "Tuesday", "The Rise of African Tech Giants", "Main Content"),
        ("2024-10-23", "Wednesday", "Challenge: Design a simple chatbot!", "Challenge"),
        ("2024-10-25", "Friday", "Feedback/Conversations", "Feedback"),
        ("2024-10-28", "Monday", "AI in healthcare", "Main Content"),
        ("2024-10-30", "Wednesday", "Challenge: Create a data visualization", "Challenge"),
        ("2024-11-01", "Friday", "Feedback/Conversations", "Feedback"),
        ("2024-11-01", "Friday", '"Ask Me Anything" with a Senior Developer', "QA Event"),
        
        # November 2024
        ("2024-11-04", "Monday", "Cloud Computing: Transforming Nigerian Businesses", "Main Content"),
        ("2024-11-06", "Wednesday", "Challenge: Build a simple API", "Challenge"),
        ("2024-11-08", "Friday", "Feedback/Conversations", "Feedback"),
        ("2024-11-11", "Monday", "Blockchain beyond Cryptocurrency: Nigerian Use Cases", "Main Content"),
        ("2024-11-13", "Wednesday", "Challenge: Create a machine learning Model", "Challenge"),
        ("2024-11-15", "Friday", "Feedback/Conversations", "Feedback"),
        ("2024-11-18", "Monday", "From Rejection to Success: Nigerian Tech Inspirations", "Main Content"),
        ("2024-11-20", "Wednesday", "Challenge: Optimize Your LinkedIn Profile", "Challenge"),
        ("2024-11-22", "Friday", "Feedback/Conversations", "Feedback"),
        ("2024-11-25", "Monday", "The Power of Tech Communities in Nigeria", "Main Content"),
        ("2024-11-27", "Wednesday", "Challenge: Contribute to an Open Source Project", "Challenge"),
        ("2024-11-29", "Friday", "Feedback/Conversations", "Feedback"),
        ("2024-11-29", "Friday", '"Tech Trends Q&A" with Industry Expert', "QA Event"),
        ("2024-11-29", "Friday", '"Advanced Git Workshop"', "Upskilling Event"),
        
        # December 2024
        ("2024-12-02", "Monday", "Soft Skills: The Secret Weapon in Nigerian Tech", "Main Content"),
        ("2024-12-04", "Wednesday", "Challenge: Create a Tech Blog Post", "Challenge"),
        ("2024-12-06", "Friday", "Feedback/Conversations", "Feedback"),
        ("2024-12-09", "Monday", "Problem-Solving: The Heart of Nigerian Tech Innovation", "Main Content"),
        ("2024-12-11", "Wednesday", "Challenge: Design Your Learning Roadmap", "Challenge"),
        ("2024-12-13", "Friday", "Feedback/Conversations", "Feedback"),
        ("2024-12-16", "Monday", "Year in Review: Nigerian Tech Milestones 2024", "Main Content"),
        ("2024-12-18", "Wednesday", "Challenge: Create a 2025 Tech Goals Vision Board", "Challenge"),
        ("2024-12-20", "Friday", "Feedback/Conversations", "Feedback"),
        ("2024-12-23", "Monday", "Holiday Special: Tech for Social Good in Nigeria", "Main Content"),
        ("2024-12-25", "Wednesday", "Challenge: Design a Tech-Inspired Holiday Greeting", "Challenge"),
        ("2024-12-27", "Friday", "Feedback/Conversations", "Feedback"),
        ("2024-12-27", "Friday", '"Year-End Reflections" with Community Leaders', "QA Event"),
        ("2024-12-27", "Friday", '"Data Science for Beginners"', "Upskilling Event")
    ]

    # Create DataFrame
    df = pd.DataFrame(calendar_data, columns=['Date', 'Day', 'Topic', 'Event Type'])

    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Sort by date
    df = df.sort_values('Date')

    # Save to Excel
    excel_file = 'specific_community_calendar.xlsx'
    df.to_excel(excel_file, index=False, engine='openpyxl')
    print(f"Calendar has been saved to {excel_file}")

    # Create a separate sheet for ongoing activities
    ongoing_activities = pd.DataFrame([
        ("Weekly", "Virtual coffee chats for networking"),
        ("Bi-weekly", "Talent showcase spotlighting community members"),
        ("Monthly", "Peer code review sessions"),
        ("Ongoing", "Mentorship program matching junior and senior developers")
    ], columns=['Frequency', 'Activity'])

    # Create a Pandas Excel writer using openpyxl as the engine
    with pd.ExcelWriter(excel_file, engine='openpyxl', mode='a') as writer:
        ongoing_activities.to_excel(writer, sheet_name='Ongoing Activities', index=False)

    print(f"Ongoing activities have been added to {excel_file}")

# Run the function
generate_specific_calendar_excel()