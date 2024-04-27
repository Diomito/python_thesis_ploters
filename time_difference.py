import pandas as pd
import tkinter as tk
from tkinter import filedialog
import re

# Function to open a file dialog and return the selected file path
def pick_csv_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    return file_path

# Pick the CSV file
csv_file = pick_csv_file()

# Load the CSV file into a DataFrame
df = pd.read_csv(csv_file, sep=',')

given_time = input('Put the given time: ')

# Function to calculate the time difference between the first and last seconds
def calculate_time_difference():
    #this code return the first_second when the warning starts
    time_list = df['Time']

    # Define a function to extract the time part from each string
    def extract_time(time_str):
        match = re.search(r'\d{2}:\d{2}:\d{2}', str(time_str))
        if match:
            return match.group()
        else:
            return None

    # Iterate over the list and search for the given time
    for time_str in time_list:
        time_part = extract_time(time_str)
        if time_part == given_time:
            time_part = re.search(r'\d{2}:\d{2}:\d{2}', time_str).group()
            break
    else:
        print("Time not found")

    # Initialize a variable to store the index of the matched time string
    matched_index = None

    # Iterate over the list and search for the given time
    for index, time_str in enumerate(time_list):
        if given_time in str(time_str):
            matched_index = index
            break

    # Check if the given time was found
    if matched_index is not None:
        # Get the corresponding seconds value from the 'Seconds' column
        first_seconds = df.loc[matched_index, 'Seconds']
    else:
        print("Time not found")

    #This code returns the last_second when the drive touch the wheel
    # Convert the 'Time' column to strings if it's not already in string format
    df['Time'] = df['Time'].astype(str)

    # Find the index corresponding to the given time
    start_index = df[df['Time'].str.contains(given_time)].index.tolist()[0]

    # Initialize a flag to indicate whether 'Hands on steering wheel' is found
    hands_on_steering_wheel_found = False

    # Iterate over the rows starting from the given time
    for index, row in df.iloc[start_index:].iterrows():
        if row['Hands on steering wheel:'] in [1, 2]:
            last_second = row['Seconds']
            hands_on_steering_wheel_found = True
            break
    # If 'Hands on steering wheel' is not found after the given time
    if not hands_on_steering_wheel_found:
        print("No occurrence of 'Hands on steering wheel' being 1 or 2 found after the given time.")
    
    return last_second - first_seconds

# Calculate the time difference
time_difference = calculate_time_difference()

# Create a DataFrame to store the result
result_df = pd.DataFrame({'Time Difference': [time_difference]})

# Prompt the user to select the output file path
output_file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

# If the user cancels the dialog, exit the script
if not output_file_path:
    print("Operation canceled. Exiting the script.")
    exit()

# Append the result DataFrame to the selected CSV file
result_df.to_csv(output_file_path, mode='a', header=False, index=False)

print(f"Time difference appended to '{output_file_path}'")