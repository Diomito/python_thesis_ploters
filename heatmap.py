import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import filedialog

def generate_heatmap(csv_file_path):
	df = pd.read_csv(csv_file_path, sep=',')
	plt.figure(figsize=(16, 12), dpi=100)
	sns.kdeplot(x=df['fixation x [px]'], y=df['fixation y [px]'], cmap="Reds", fill=True, bw_adjust=.5)
	plt.gca().invert_yaxis()
	plt.xlim([0, 1600])
	plt.ylim([1200, 0])
	plt.xlabel('Fixation X [px]')
	plt.ylabel('Fixation Y [px]')
	plt.title('Heatmap of Fixation Points')
	plt.show()

def main():
	# Set up the Tkinter root window
	root = tk.Tk()
	root.withdraw() # We don't want a full GUI, so keep the root window from appearing

	# Show an "Open" dialog box and return the path to the selected file
	file_path = filedialog.askopenfilename()
	
	# Check if a file was selected
	if file_path:
		generate_heatmap(file_path)

if __name__ == "__main__":
	main()
