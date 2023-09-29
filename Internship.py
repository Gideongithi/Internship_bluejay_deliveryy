import pandas as pd
from datetime import datetime, timedelta

consecutive_days_threshold = 7
time_between_shifts_threshold = 10  # in hours
single_shift_duration_threshold = 14  # in hours
short_break_threshold = 1  # in hours


file_path = r"C:\Users\Admin\Downloads\Assignment_Timecard.xlsx"  
df = pd.read_excel(file_path)

df.sort_values(by=["Employee Name", "Time"], inplace=True)

employee_to_check = input("Enter the name of the employee you want to check: ")

consecutive_days_count = 0
last_employee_name = None

def time_str_to_hours(time_str):
    if isinstance(time_str, str) and ':' in time_str:
        time_format = '%H:%M:%S' if len(time_str.split(':')) == 3 else '%H:%M'
        time_obj = datetime.strptime(time_str, time_format)
        return time_obj.hour + time_obj.minute / 60 + time_obj.second / 3600
    elif isinstance(time_str, (int, float)):
        return float(time_str)
    else:
        return None

for index, row in df[df["Employee Name"] == employee_to_check].iterrows():
    employee_name = row["Employee Name"]
    position_status = row["Position Status"]
    time_in = row["Time"]
    time_out = row["Time Out"]
    timecard_hours = time_str_to_hours(row["Timecard Hours (as Time)"])

    if timecard_hours is None:
        continue

    if employee_name != last_employee_name:
        consecutive_days_count = 1  
    else:
        consecutive_days_count += 1

    if consecutive_days_count >= consecutive_days_threshold:
        print(f"{employee_name} ({position_status}): Worked for {consecutive_days_count} consecutive days")

    if last_employee_name == employee_name and last_time_out is not None:
        time_between_shifts = (time_in - last_time_out).total_seconds() / 3600  
        if 1 < time_between_shifts < time_between_shifts_threshold:
            print(f"{employee_name} ({position_status}): Had a short break between shifts")

    if timecard_hours > single_shift_duration_threshold:
        print(f"{employee_name} ({position_status}): Worked for more than {single_shift_duration_threshold} hours in a single shift")

    last_employee_name = employee_name
    last_time_out = time_out
