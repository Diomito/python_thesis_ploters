import pandas as pd
import os
import uuid
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as messagebox

def read_file(filepath, save_directory):
    df = pd.read_csv(filepath, sep=',')

    df['System Time'] = pd.to_datetime(df['System Time'])

    df['Date'] = df['System Time'].dt.date
    df['Time'] = df['System Time'].dt.time
    df['Time'] = df['Time'].astype(str)
    df['Time'] = pd.to_timedelta(df['Time'])

    time_differences = []

    for i in df.index:
        difference_seconds = (df['Time'].iloc[-1] - df['Time'].iloc[i]).total_seconds()
        time_differences.append(difference_seconds)

    time_differences.sort()

    df['Seconds'] = time_differences
    
    old_name = os.path.basename(filepath)
    unique_filename = (f"new_{old_name}")    
    file_path = os.path.join(save_directory, unique_filename)
    df.to_csv(file_path, index=False)
    return file_path

def main():
    root = tk.Tk()
    root.withdraw()

    while True:
        file_path = filedialog.askopenfilename()
        
        if file_path:
            save_directory = filedialog.askdirectory(title="Select directory to save processed file")
            if save_directory:
                processed_file_path = read_file(file_path, save_directory)
                print(f"Processed file saved at: {processed_file_path}")
                response = messagebox.askyesno("Continue?", "Do you want to continue using the program with other files?")
                if not response:
                    break
        else:
            break

if __name__ == "__main__":
    main()