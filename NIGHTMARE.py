import numpy as np
import sounddevice as sd
import wavio
import librosa
import tkinter as tk
from tkinter import messagebox
from sklearn import svm
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import speech_recognition as sr
import pyttsx3
import subprocess
import sys
import pytesseract
from PIL import ImageGrab
import pytesseract

# Set the path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to extract MFCC features
def extract_mfcc(file_path):
    y, sr = librosa.load(file_path, sr=44100)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    return np.mean(mfcc.T, axis=0)

# Function to load features from audio files
def load_audio_files(file_paths):
    features = []
    for file_path in file_paths:
        mfcc_features = extract_mfcc(file_path)
        features.append(mfcc_features)
    return np.array(features)

# Function to recognize and transcribe speech
def transcribe_speech(file_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            return text
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio."
    except sr.RequestError as e:
        return f"Could not request results; {e}"

# Function to handle system commands
def execute_command(command):
    global window  # Declare window as global
    if "open command prompt" in command.lower() or "open cmd" in command.lower():
        subprocess.Popen("cmd.exe")
        response = "Opening Command Prompt"
    elif "open file explorer" in command.lower():
        subprocess.Popen("explorer.exe")
        response = "Opening File Explorer"
    elif "open control panel" in command.lower():
        subprocess.Popen("control.exe")
        response = "Opening Control Panel"
    elif "open settings" in command.lower():
        subprocess.Popen("start ms-settings:", shell=True)
        response = "Opening Settings"
    elif "open whatsapp" in command.lower():
        subprocess.Popen("C:\\Path\\To\\WhatsApp.exe")  # Adjust the path
        response = "Opening WhatsApp"
    elif "open opera" in command.lower():
        subprocess.Popen("C:\\Path\\To\\Opera.exe")  # Adjust the path
        response = "Opening Opera Browser"
    elif "open notepad" in command.lower():
        subprocess.Popen("notepad.exe")
        response = "Opening Notepad"
    elif "open calculator" in command.lower():
        subprocess.Popen("calc.exe")
        response = "Opening Calculator"
    elif "read screen" in command.lower():
        read_screen_content()
        return
    elif "close the program" in command.lower() or "exit nightmare" in command.lower():
        response = "Closing NIGHTMARE."
        print(response)
        speak(response)
        window.destroy()  # Terminate the program
        sys.exit()  # Ensure program exits
    else:
        response = "Command not recognized."
    
    print(response)
    engine.say(response)
    engine.runAndWait()

# Function to handle button click event
def on_listen_button_click():
    filename = "temp_recording.wav"
    record_audio(filename)  # Record audio
    command = transcribe_speech(filename)  # Transcribe audio

    # Respond based on the recognized command
    if command:
        print(f"You said: {command}")
        engine.say(f"You said: {command}")
        engine.runAndWait()
        execute_command(command)
    else:
        messagebox.showinfo("Recognition", "Could not recognize your voice.")

# Record audio function (you can replace this with loading pre-recorded audio)
def record_audio(filename, duration=5):
    print("Recording...")
    audio = sd.rec(int(duration * 44100), samplerate=44100, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    wavio.write(filename, audio, 44100, sampwidth=2)
    print("Recording complete.")
    
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to read screen content
def read_screen_content():
    # Capture the entire screen
    screen = ImageGrab.grab()
    screen.save("screenshot.png")  # Save the screenshot to a file (optional)

    # Use pytesseract to extract text from the image
    text = pytesseract.image_to_string(screen)
    print(text)  # Print the text to the console
    speak(text)  # Read the text aloud

# Function to authenticate using a voice command
def authenticate_password():
    def check_password():
        filename = "temp_password.wav"
        record_audio(filename, duration=5)  # Record audio for 5 seconds
        password = transcribe_speech(filename)  # Transcribe audio to text
        
        if password.lower() == "nightmare":
            auth_window.destroy()
            # Proceed to main application
            main_app()
        else:
            messagebox.showerror("Authentication Failed", "Incorrect password. Please try again.")
            speak("Incorrect password. Please try again.")

    auth_window = tk.Tk()
    auth_window.title("Voice Password Authentication")
    tk.Label(auth_window, text="Say 'Hi NIGHTMARE' to authenticate:").pack(pady=10)
    tk.Button(auth_window, text="Authenticate", command=check_password).pack(pady=10)
    auth_window.mainloop()

# Main application function
def main_app():
    global window  # Declare window as global
    window = tk.Tk()
    window.title("Voice Command Recognition")
    speak("Welcome master Joel")

    # Create a button to listen for commands
    listen_button = tk.Button(window, text="Listen", command=on_listen_button_click, height=2, width=20)
    listen_button.pack(pady=20)

    # Start the Tkinter event loop
    window.mainloop()

# Main function to run the program
def main():
    authenticate_password()

if __name__ == "__main__":
    main()
