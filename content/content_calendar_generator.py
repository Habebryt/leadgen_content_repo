import pandas as pd
from datetime import datetime, timedelta

def generate_calendar_excel():
    # Define the start date
    start_date = datetime(2024, 10, 22)

    # Create lists to store the data
    dates = []
    days = []
    topics = []
    event_types = []

    # Generate data for each week
    current_date = start_date
    while current_date <= datetime(2024, 12, 31):
        # Monday
        dates.append(current_date.strftime('%Y-%m-%d'))
        days.append(current_date.strftime('%A'))
        topics.append("Weekly Topic")
        event_types.append("Main Content")

        # Wednesday
        wed_date = current_date + timedelta(days=2)
        dates.append(wed_date.strftime('%Y-%m-%d'))
        days.append(wed_date.strftime('%A'))
        topics.append("Weekly Challenge")
        event_types.append("Challenge")

        # Friday
        fri_date = current_date + timedelta(days=4)
        dates.append(fri_date.strftime('%Y-%m-%d'))
        days.append(fri_date.strftime('%A'))
        topics.append("Feedback/Conversations")
        event_types.append("Feedback")

        # Check if it's the last week of the month for QA and Upskilling events
        if current_date.month != (current_date + timedelta(days=7)).month:
            # QA Event
            dates.append(fri_date.strftime('%Y-%m-%d'))
            days.append(fri_date.strftime('%A'))
            topics.append("Monthly QA Event")
            event_types.append("QA Event")

            # Upskilling Event
            dates.append(fri_date.strftime('%Y-%m-%d'))
            days.append(fri_date.strftime('%A'))
            topics.append("Monthly Upskilling Event")
            event_types.append("Upskilling Event")

        # Move to next week
        current_date += timedelta(days=7)

    # Create DataFrame
    df = pd.DataFrame({
        'Date': dates,
        'Day': days,
        'Topic': topics,
        'Event Type': event_types
    })

    # Save to Excel
    excel_file = 'community_calendar.xlsx'
    df.to_excel(excel_file, index=False, engine='openpyxl')
    print(f"Calendar has been saved to {excel_file}")

# Run the function
generate_calendar_excel()