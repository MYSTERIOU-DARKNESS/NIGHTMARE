# NIGHTMARE
NIGHTMARE: Voice Command System
NIGHTMARE is a voice command system that allows you to interact with your computer through voice commands. It can perform actions like opening applications (e.g., Notepad, Command Prompt, WhatsApp), reading screen content using OCR, and more. The system uses voice authentication, natural language processing (NLP), and machine learning to recognize commands.

Prerequisites
Before running the program, ensure that you have the following dependencies installed:

Python 3.x (Make sure you have the correct version installed)

Download Python from: Python.org
Required Python Libraries: You can install the necessary libraries using pip. 
Open a terminal or command prompt and run the following command:
  pip install numpy sounddevice wavio librosa sklearn pyttsx3 speechrecognition pytesseract pillow opencv-python

Tesseract OCR:

Install Tesseract OCR to enable text extraction from images (screen content). You can download it from here.

After installation, make sure to update the path to the Tesseract executable in your script:
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


