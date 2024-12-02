import pandas as pd
from datetime import datetime, timedelta

def generate_comprehensive_calendar_csv():
    # Define the calendar data
    calendar_data = [
        # October 2024
        ("2024-10-22", "Tuesday", "Community", "The Rise of African Tech Giants", "WhatsApp: Discussion prompt, Twitter: Thread on African tech success stories"),
        ("2024-10-22", "Tuesday", "TaaS", "LinkedIn post on tech talent trends in Africa", "LinkedIn"),
        ("2024-10-23", "Wednesday", "Community", "Challenge: Design a simple chatbot!", "WhatsApp: Challenge announcement, Twitter: Tips for chatbot design"),
        ("2024-10-23", "Wednesday", "Solutions", "Blog post on 'Chatbots for Customer Service'", "Blog"),
        ("2024-10-24", "Thursday", "Data2Employ", "Instagram story featuring success stories", "Instagram"),
        ("2024-10-25", "Friday", "Community", "Feedback/Conversations", "WhatsApp: Open discussion"),
        ("2024-10-25", "Friday", "Newsletter", "Monthly TaaS update", "Email"),
        
        # Add more entries for subsequent weeks...
        
        # December 2024 (last week)
        ("2024-12-23", "Monday", "Community", "Holiday Special: Tech for Social Good in Nigeria", "WhatsApp: Call for tech-for-good ideas, Facebook: Post on Data2Bots' social impact initiatives"),
        ("2024-12-25", "Wednesday", "Community", "Challenge: Design a Tech-Inspired Holiday Greeting", "WhatsApp: Challenge announcement, Twitter: Showcase best greetings"),
        ("2024-12-25", "Wednesday", "TaaS", "LinkedIn post on work-life balance in tech", "LinkedIn"),
        ("2024-12-27", "Friday", "Community", "Feedback/Conversations", "WhatsApp: Open discussion"),
        ("2024-12-27", "Friday", "Newsletter", "Year-end comprehensive update (all value streams)", "Email"),
        ("2024-12-27", "Friday", "QA Event", '"Year-End Reflections" with Community Leaders', "WhatsApp: Live Q&A session, LinkedIn: Post-event summary"),
        ("2024-12-27", "Friday", "Upskilling Event", '"Data Science for Beginners"', "WhatsApp: Workshop announcement and registration, Twitter: Live-tweeting key learnings")
    ]

    # Create DataFrame
    df = pd.DataFrame(calendar_data, columns=['Date', 'Day', 'Category', 'Activity', 'Platforms'])

    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Sort by date
    df = df.sort_values('Date')

    # Save to CSV
    csv_file = 'comprehensive_data2bots_calendar.csv'
    df.to_csv(csv_file, index=False)
    print(f"Calendar has been saved to {csv_file}")

    # Create a separate DataFrame for ongoing activities
    ongoing_activities = pd.DataFrame([
        ("Weekly", "Virtual coffee chats for networking", "WhatsApp coordination"),
        ("Bi-weekly", "Talent showcase spotlighting community members", "LinkedIn, Instagram"),
        ("Monthly", "Peer code review sessions", "GitHub, WhatsApp coordination"),
        ("Ongoing", "Mentorship program matching junior and senior developers", "LinkedIn, WhatsApp")
    ], columns=['Frequency', 'Activity', 'Platforms'])

    # Save ongoing activities to CSV
    ongoing_csv_file = 'ongoing_activities.csv'
    ongoing_activities.to_csv(ongoing_csv_file, index=False)
    print(f"Ongoing activities have been saved to {ongoing_csv_file}")

if __name__ == "__main__":
    generate_comprehensive_calendar_csv()