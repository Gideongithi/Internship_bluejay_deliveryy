import pandas as pd
from datetime import datetime, timedelta

def check_conditions(row):
    # Condition 1: Worked for 7 consecutive days
    days_worked = len(pd.date_range(row['Pay Cycle Start Date'], row['Pay Cycle End Date']))
    if days_worked >= 7:
        return True
    
    # Condition 2: Less than 10 hours between shifts, but more than 1 hour
    time_out = datetime.strptime(row['Time Out'], '%H:%M')
    prev_time_out = datetime.strptime(prev_shift['Time'], '%H:%M')
    time_diff = (time_out - prev_time_out).seconds // 3600
    if time_diff < 10 and time_diff > 1:
        return True
    
    # Condition 3: Worked for more than 14 hours in a single shift
    timecard_hours = float(row['Timecard Hours (as Time)'])
    if timecard_hours > 14:
        return True
    
    return False

# Load the CSV file into a DataFrame
csv_file_path = 'input.csv'
data = pd.read_csv(csv_file_path)

# Initialize variables to keep track of the previous shift information
prev_shift = None

# Iterate through the records and apply the conditions
for index, row in data.iterrows():
    if prev_shift is None or row['Employee Name'] != prev_shift['Employee Name']:
        prev_shift = row
        continue
    
    if check_conditions(row):
        print(f"Employee Name: {row['Employee Name']}, Position ID: {row['Position ID']}, Position Status: {row['Position Status']}")

    prev_shift = row
