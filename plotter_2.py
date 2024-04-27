import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import messagebox
import statistics
import numpy as np
import re

#beam data functions
def browse_Main_data():
    Main_file_path.set(filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")]))
    
def calculate_stats(data):
    stats = {}
    stats['Minimum'] = np.min(data)
    stats['Maximum'] = np.max(data)
    stats['Average'] = np.mean(data)
    stats['Standard Deviation'] = np.std(data)
    stats['Median'] = statistics.median(data)
    return stats

def plot_Main_data():
    filepath = Main_file_path.get()
    if not filepath:
        messagebox.showerror("Error", "Please select a file first!")
        return
    try:
        df = pd.read_csv(filepath, sep=',')

        plt.figure(figsize=(12, 6))
        plt.subplot(2, 1, 1)
        plt.plot(df['Seconds'], df['Speed (km/h)'], label='Speed (km/h)')
        plt.plot(df['Seconds'], df['Throttle'], label='Throttle')
        plt.plot(df['Seconds'], df['Brake'], label='Brake')
        plt.plot(df['Seconds'], df['Steering Angle'], label='Steering Angle')
        plt.xlabel('Time')
        plt.ylabel('Values')
        plt.title('BeamNG Data')
        plt.legend()
        plt.grid(True)
        plt.subplot(2, 1, 2)
        plt.plot(df['posX'], df['posY'])
        plt.xlabel('posX')
        plt.ylabel('posY')
        plt.title('Trajectory')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        # Display statistics for each variable in a message box
        stats_message = ''
        for column in df.columns:
            if df[column].dtype in [np.float64, np.int64]:
                stats = calculate_stats(df[column])
                stats_message += f"\n\nStatistics for {column}:\n"
                for stat, value in stats.items():
                    stats_message += f"{stat}: {value:.2f}\n"

        root = tk.Tk()
        root.withdraw()
        root.clipboard_clear()
        root.clipboard_append(stats_message)
        root.update()
        root.destroy()
        messagebox.showinfo("Data Statistics", stats_message)
        messagebox.showinfo("Data Statistics", "Statistics have been copied to clipboard. You can paste it anywhere.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

#Hand data functions
def browse_hand_data():
    Hand_file_path.set(filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")]))

def plot_Hand_data():
    try:
        hand_df = pd.read_csv(Hand_file_path.get(), sep=',')
        hand_df.columns = hand_df.columns.str.strip()        
        plt.figure(figsize=(10, 6))        
        plt.bar(hand_df['Seconds'], hand_df['Hands on steering wheel:'], label='Hands on steering wheel')        
        hand_df['Hands on Navigation:'] = hand_df['Hands on Navigation:'].map({False: 0, True: 1})
        hand_df['Hands on Shifter:'] = hand_df['Hands on Shifter:'].map({False: 0, True: 1})
        plt.plot(hand_df['Seconds'], hand_df['Hands on Navigation:'], label='Hands on Navigation')
        plt.plot(hand_df['Seconds'], hand_df['Hands on Shifter:'], label='Hands on Shifter')        
        plt.xlabel('Time')
        plt.ylabel('Values')
        plt.title('Hand Data')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.gca().xaxis.set_major_locator(plt.MaxNLocator(nbins=10))        
        plt.tight_layout()
        plt.show()
    except FileNotFoundError:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

#Heart rate data functions
def browse_heart_data():
    Heart_file_path.set(filedialog.askopenfilename(filetypes=[("Log files", "*.log")]))

def parse_heart_data():
    log_line_regex = r'(\d{2}:\d{2}:\d{2},\d{3}) .* HeartRate = (\d+)'
    timestamps = []
    heart_rates = []

    filepath = Heart_file_path.get()  # Assuming Heart_file_path is defined elsewhere
    if not filepath:
        messagebox.showerror("Error", "Please select a file first!")
        return None

    try:
        with open(filepath, 'r') as file:
            for line in file:
                match = re.search(log_line_regex, line)
                if match:
                    timestamp = pd.to_datetime(match.group(1), format='%H:%M:%S,%f')
                    heart_rate = int(match.group(2))
                    timestamps.append(timestamp)
                    heart_rates.append(heart_rate)
        return pd.DataFrame({'Timestamp': timestamps, 'HeartRate': heart_rates})
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        return None

def copy_to_clipboard(text):
    root = tk.Tk()
    root.withdraw()
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()
    root.destroy()

def plot_heart_data():
    parsed_data = parse_heart_data()
    if parsed_data is None:
        messagebox.showerror("Error", "Failed to parse heart data.")
        return
    
    timestamps = parsed_data['Timestamp']
    # Get the start time
    start_time = timestamps.min()
    # Calculate time difference in seconds
    parsed_data['Seconds'] = (timestamps - start_time).dt.total_seconds()  
    # Extract heart rates from parsed_data
    heart_rates = parsed_data['HeartRate']  
    
    max_hr = np.max(heart_rates)
    min_hr = np.min(heart_rates)
    avg_hr = np.mean(heart_rates)
    sd_hr = np.std(heart_rates)
    md_hr = statistics.median(heart_rates)

    plt.figure(figsize=(10, 6))
    plt.plot(parsed_data['Seconds'], parsed_data['HeartRate'], marker='o', linestyle='-')
    plt.title('Heart Rate Over Time')
    plt.xlabel('Time (seconds from start)')
    plt.ylabel('Heart Rate (bpm)')
    plt.tight_layout()
    plt.show()


    stats_message = f"Maximum Heart Rate: {max_hr} bpm\n" \
                    f"Minimum Heart Rate: {min_hr} bpm\n" \
                    f"Average Heart Rate: {avg_hr:.2f} bpm\n" \
                    f"Standard Deviation: {sd_hr:.2f}\n" \
                    f"Median Heart Rate: {md_hr} bpm"
    
    root = tk.Tk()
    root.withdraw()
    root.clipboard_clear()
    root.clipboard_append(stats_message)
    root.update()
    root.destroy()

    messagebox.showinfo("Heart Rate Statistics", stats_message)
    messagebox.showinfo("Heart Rate Statistics", "Statistics have been copied to clipboard. You can paste it anywhere.")

root = tk.Tk()
root.title("joined data plotter")
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Main data buttons
Main_file_path = tk.StringVar()
browse_button_main = tk.Button(frame, text="Browse Main File", command=browse_Main_data)
browse_button_main.grid(row=0, column=0)
plot_button_main = tk.Button(frame, text="Plot main", command=plot_Main_data)
plot_button_main.grid(row=1, column=0)
file_label_main = tk.Label(frame, textvariable=Main_file_path, width=50)
file_label_main.grid(row=2, column=0)

# Hand data buttons
Hand_file_path = tk.StringVar()
browse_button_hand = tk.Button(frame, text="Browse Hand File", command=browse_hand_data)
browse_button_hand.grid(row=3, column=0)
plot_button_hand = tk.Button(frame, text="Plot Hand", command=plot_Hand_data)
plot_button_hand.grid(row=4, column=0)
file_label_hand = tk.Label(frame, textvariable=Hand_file_path, width=50)
file_label_hand.grid(row=5, column=0)

# Heart data buttons
Heart_file_path = tk.StringVar()
browse_button_heart = tk.Button(frame, text="Browse Heart File", command=browse_heart_data)
browse_button_heart.grid(row=6, column=0)
plot_button_heart = tk.Button(frame, text="Plot Heart", command=plot_heart_data)
plot_button_heart.grid(row=7, column=0)
file_label_heart = tk.Label(frame, textvariable=Heart_file_path, width=50)
file_label_heart.grid(row=8, column=0)
root.mainloop()