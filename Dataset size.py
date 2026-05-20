import os
import wave
import tkinter as tk
from tkinter import filedialog

# set up the file dialog
root = tk.Tk()
root.withdraw()  # Hide the root window

# open the folder path dialog to select a folder containing audio files
folder_path = filedialog.askdirectory(title="Select a folder containing audio files")

if folder_path:
    total_duration = 0.0
    total_files = 0

    # Loop through all files in the selected folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".wav"):
            file_path = os.path.join(folder_path, filename)
            try:
                with wave.open(file_path, 'r') as audio_file:
                        frames = audio_file.getnframes()
                        rate = audio_file.getframerate()
                        duration = frames / float(rate)
                        total_duration += duration
                        total_files += 1
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    
    hours = int(total_duration // 3600)
    minutes = int((total_duration % 3600) // 60)
    seconds = total_duration % 60
    
    print(f"Total .wav files processed: {total_files}")
    print(f"Total duration of audio files: {hours} hours, {minutes} minutes, {seconds:.2f} seconds")

else:
    print("No folder selected.")