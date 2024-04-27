import re
import csv
from tkinter import filedialog
import tkinter as tk
import os

def process_log_file():
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),.*?HeartRate = (\d+)'

    # Use filedialog to ask for the file path
    file_path = filedialog.askopenfilename()

    # Check if the user selected a file
    if file_path:
        # Extract the name of the log file
        log_file_name = os.path.basename(file_path)
        # Generate the name for the CSV file
        csv_file_name = os.path.splitext(log_file_name)[0] + '.csv'

        # Use filedialog to ask for the save location and filename
        save_file_path = filedialog.asksaveasfilename(defaultextension=".csv", initialfile=csv_file_name)

        if save_file_path:
            with open(save_file_path, 'w', newline='') as csvfile:
                fieldnames = ['System Time', 'Heart Rate']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                
                with open(file_path, 'r') as logfile:
                    for line in logfile:
                        match = re.search(pattern, line)
                        if match:
                            system_time, heart_rate = match.groups()
                            writer.writerow({'System Time': system_time, 'Heart Rate': heart_rate})
            print("CSV file saved successfully.")
        else:
            print("No save location specified.")
    else:
        print("No file selected.")

def main():
    while True:
        process_log_file()
        user_input = input("Do you want to try a new file? (yes/no): ").lower()
        if user_input != 'yes':
            print("Exiting the program.")
            break

if __name__ == "__main__":
    main()