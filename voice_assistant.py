import pyttsx3
import tkinter as tk
from tkinter import messagebox
import wikipedia
import speech_recognition as sr
import webbrowser
import pyjokes
from datetime import datetime
from bs4 import BeautifulSoup

engine = pyttsx3.init('sapi5')  
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Set voice (0 for male, 1 for female if available)

def speak(text):
    """Function to convert text to speech"""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Function to recognize voice input"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
    except Exception as e:
        print("Sorry, I didn't catch that. Please try again.")
        speak("Sorry, I didn't catch that. Please try again.")
        return "None"
    return query.lower()

def greet():
    hour = int(datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your personal assistant. How can I help you today?")

def search_wikipedia(query):
    speak("Searching Wikipedia...")
    query = query.replace("wikipedia", "")
    try:
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)
    except Exception as e:
        speak("Sorry, I couldn't find anything on Wikipedia about that.")

def open_website(query):
    if "youtube" in query:
        webbrowser.open("youtube.com")
    elif "google" in query:
        webbrowser.open("google.com")
    elif "website" in query:
        url = query.split("open")[-1].strip()
        webbrowser.open(f"https://{url}")
    else:
        speak("I didn't understand which website to open.")

def tell_joke():
    joke = pyjokes.get_joke()
    print(joke)
    speak(joke)

def get_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    speak(f"The current time is {current_time}")

# def send_sms():
#     account_sid = "YOUR_TWILIO_SID"  # Replace with your Twilio SID
#     auth_token = "YOUR_TWILIO_AUTH_TOKEN"  # Replace with your Twilio Auth Token
#     client = Client(account_sid, auth_token)
    
#     message = client.messages.create(
#         body="Hello from your Python Voice Assistant!",
#         from_="YOUR_TWILIO_PHONE_NUMBER",  # Replace with your Twilio number
#         to="RECIPIENT_PHONE_NUMBER"  # Replace with recipient's number
#     )
#     speak("Message sent successfully!")

def main():
    greet()
    while True:
        query = listen()
        
        if query == "none":
            continue
        
        # Exit command
        if "exit" in query or "stop" in query:
            speak("Goodbye!")
            break
        
        # Command processing
        elif "wikipedia" in query:
            search_wikipedia(query)
        elif "open" in query:
            open_website(query)
        elif "joke" in query:
            tell_joke()
        elif "time" in query:
            get_time()
        else:
            speak("Sorry, I don't know how to help with that yet.")

if __name__ == "__main__":
    main()

root = tk.Tk()
root.title("Voice Assistant")
root.geometry("300x200")

def start_assistant():
    messagebox.showinfo("Voice Assistant", "Assistant is starting...")
    main()

start_button = tk.Button(root, text="Start Assistant", command=start_assistant)
start_button.pack(pady=20)

exit_button = tk.Button(root, text="Exit", command=root.quit)
exit_button.pack(pady=20)

root.mainloop()