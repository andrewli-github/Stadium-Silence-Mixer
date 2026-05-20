# audio manipulating library
from pydub import AudioSegment
import tkinter as tk
from tkinter import filedialog

def time_to_milliseconds(time_str):
    """Convert a time string in the format 'HH:MM:SS' to milliseconds."""
    hours, minutes, seconds = map(int, time_str.split(':'))
    return ((hours * 60 + minutes) * 60 + seconds) * 1000

# Load the audio file
# set up the file dialog
root = tk.Tk()
root.withdraw()  # Hide the root window

# open the file dialog to select an audio file
file_path = filedialog.askopenfilename(
    title="Select an audio file", 
    filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")]
)

if file_path:
    audio = AudioSegment.from_file(file_path)

    # Start and end times
    start_time_str = "01:36:40"  # in HH:MM:SS format
    end_time_str = "01:41:12"    # in HH:MM:SS format

    start_time = time_to_milliseconds(start_time_str)
    end_time = time_to_milliseconds(end_time_str)
    chopped_audio = audio[start_time:end_time]

    # export audio file
    chopped_audio.export("chopped " + file_path.split("/")[-1], format="wav")
    print("Audio segment sliced and saved as 'chopped_audio.wav'")

else:
    print("No file selected.")
