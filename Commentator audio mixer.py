import random  # Added to allow mathematical randomization
import tkinter as tk
from tkinter import filedialog
from pydub import AudioSegment  

# Define the amount to lower the volume (in dB)
crowd_lowerdB = 13  
commentator_lowerdB = 4

# set up the file dialog
root = tk.Tk()
root.withdraw()  # Hide the root window

# Ask for crowd audio file
print("Select the crowd audio file:")
crowd_audio_path = filedialog.askopenfilename(
    title="Select Crowd Audio File", 
    filetypes=[("Audio Files", "*.mp3 *.wav")]
)

# Ask for commentator audio file
print("Select the commentator audio file:")
commentator_audio_path = filedialog.askopenfilename(
    title="Select Commentator Audio File", 
    filetypes=[("Audio Files", "*.mp3 *.wav")]
)

if crowd_audio_path and commentator_audio_path:
    # Load the audio files
    crowd_audio = AudioSegment.from_file(crowd_audio_path)
    commentator_audio = AudioSegment.from_file(commentator_audio_path)

    # Adjust the volume of the audio files 
    adjusted_crowd = crowd_audio - crowd_lowerdB
    adjusted_commentator = commentator_audio - commentator_lowerdB

    print("Generating natural pacing for the commentator...")
    
    # Pacing logic
    paced_commentator = AudioSegment.empty()
    current_position = 0
    commentator_length = len(adjusted_commentator)

    while current_position < commentator_length:
        # Commentator speaks for a random duration (e.g., 3 to 10 seconds)
        speak_duration = random.randint(3000, 10000) 
        
        # Slice that chunk from the original, volume-adjusted commentator audio
        chunk = adjusted_commentator[current_position : current_position + speak_duration]
        
        # Add a random pause after the chunk (e.g., 2 to 5 seconds)
        pause_duration = random.randint(1000, 3000)
        silence = AudioSegment.silent(duration=pause_duration)
        
        # Append the chunk and the pause to our new paced commentator track
        paced_commentator += chunk + silence
        
        # Move the current position forward by the duration of the chunk
        current_position += speak_duration
        
        # If the next chunk would exceed the length of the commentator audio, break out of the loop
        if current_position + speak_duration > len(adjusted_commentator):
            break

    # Trim the newly paced voice to match the exact length of the crowd audio
    paced_commentator = paced_commentator[:len(adjusted_crowd)]

    print("Mixing audio tracks together...")
    
    # Mix the newly paced audio file onto the adjusted crowd file
    mixed_audio = adjusted_crowd.overlay(paced_commentator)

    # Export the mixed audio file
    output_path = "input_mixed.wav"  # Updated to match ML dataset naming standards
    mixed_audio.export(output_path, format="wav")
    print(f"Success! Mixed audio saved as '{output_path}'")
else:
    print("Audio files not selected. Please select both crowd and commentator audio files.")