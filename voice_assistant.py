import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtGui import QIcon
import pyttsx3
import speech_recognition as sr
import webbrowser
import pyjokes
from datetime import datetime
import wikipedia

# Initialize text-to-speech
engine = pyttsx3.init('sapi5')  #for windows
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

class VoiceAssistantGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.listening = False
        
    def initUI(self):
        # Window settings
        self.setWindowTitle("Python-based Voice Assistant")
        self.setWindowIcon(QIcon("logo.png"))
        self.setGeometry(500, 350, 600, 500)    #window size
        self.setStyleSheet("""
            background-color: #1F2A44;  /* Darker blue-gray */
            border-radius: 10px;
        """)
        
        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)  # Increased spacing between elements
        

        # Title
        layout.addSpacing(20)
        title = QLabel("Voice Assistant")
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setStyleSheet("color: #E6E6FA;")  # Soft lavender text
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(30)  # Extra spacing after title
        

        # Status label
        self.status = QLabel("Press 'Start' to begin")
        self.status.setFont(QFont("Arial", 12))
        self.status.setStyleSheet("""
            color: #A9B7C6;  /* Light grayish-blue */
            background-color: #2A3555;  /* Subtle background */
            padding: 10px;
            border-radius: 15px;
        """)
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setWordWrap(True)  # Allow text wrapping
        layout.addWidget(self.status)
        layout.addSpacing(20)  # Spacing before buttons
        

        # Button container for horizontal alignment
        button_layout = QVBoxLayout()
        button_layout.setSpacing(20)  # Space between buttons
        

        # Start button
        self.start_btn = QPushButton("Start")
        self.start_btn.setFont(QFont("Arial", 10))
        self.start_btn.setFixedSize(130, 60)    #button size
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #0c54cf;
                color: white;
                font-size: 20px;
                padding: 10px;
                border-radius: 25px;
            }
            QPushButton:hover {
                background-color: #023ca1;  /* Darker blue on hover */
            }
        """)
        self.start_btn.clicked.connect(self.toggle_listening)
        button_layout.addWidget(self.start_btn, alignment=Qt.AlignCenter)
        

        # Stop button
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setFont(QFont("Arial", 10))
        self.stop_btn.setFixedSize(130, 60) #button size
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff0000;
                color: white;
                padding: 10px;
                border-radius: 25px;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: #bd0202;  
            }
        """)
        self.stop_btn.clicked.connect(self.stop_assistant)
        button_layout.addWidget(self.stop_btn, alignment=Qt.AlignCenter)
        
        layout.addLayout(button_layout)
        layout.addStretch()  # Push content up, leaving space at bottom

    #speak function   
    def speak(self, text):
        engine.say(text)
        engine.runAndWait()

    #listen function  
    def listen(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.status.setText("Listening...")
            recognizer.pause_threshold = 1
            audio = recognizer.listen(source)
        
        try:
            self.status.setText("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-in')
            self.status.setText(f"You said: {query}")
            return query.lower()
        except Exception:
            self.status.setText("Sorry, I didn't catch that")
            self.speak("Sorry, I didn't catch that")
            return "none"


    #process command function
    def process_command(self, query):
        if query == "none":
            return
        
        if "exit" in query or "stop" in query:
            self.stop_assistant()
        elif "wikipedia" in query:
            self.search_wikipedia(query)
        elif "open" in query:
            self.open_website(query)
        elif "joke" in query:
            self.tell_joke()
        elif "time" in query:
            self.get_time()
        else:
            self.speak("Sorry, I don't know how to help with that yet")


    #search wikipedia function
    def search_wikipedia(self, query):
        self.speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        try:
            results = wikipedia.summary(query, sentences=2)
            self.speak("According to Wikipedia")
            self.status.setText(results)
            self.speak(results)
        except Exception:
            self.speak("Sorry, I couldn't find anything on Wikipedia")

    #open website function
    def open_website(self, query):
        if "youtube" in query:
            webbrowser.open("youtube.com")
        elif "google" in query:
            webbrowser.open("google.com")
        elif "website" in query:
            url = query.split("open")[-1].strip()
            webbrowser.open(f"https://{url}")
        else:
            self.speak("I didn't understand which website to open")


    #tell joke function
    def tell_joke(self):
        joke = pyjokes.get_joke()
        self.status.setText(joke)
        self.speak(joke)
        self.speak("Here's a joke for you!")
    

    #get time function
    def get_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.speak(f"The current time is {current_time}")
        self.status.setText(f"Time: {current_time}")


    #toggle listening function; this function is called when the user clicks the "Start" button
    def toggle_listening(self):
        if not self.listening:
            self.listening = True
            self.start_btn.setText("Listening")
            self.speak("Hello! How can I assist you today?")
            QTimer.singleShot(1000, self.process_voice)
        else:
            self.listening = False
            self.start_btn.setText("Start")
            self.status.setText("Press 'Start' to begin")


    ##process voice function; this function is called repeatedly to listen for commands
    def process_voice(self):
        if self.listening:
            query = self.listen()
            self.process_command(query)
            QTimer.singleShot(1000, self.process_voice)


    ##stop assistant function; this function is called when the user clicks the "Stop" button
    def stop_assistant(self):
        self.listening = False
        self.start_btn.setText("Start")
        self.speak("Goodbye!")
        self.status.setText("Assistant stopped")


## Main function to run the application
def main():
    app = QApplication(sys.argv)
    window = VoiceAssistantGUI()
    window.show()
    sys.exit(app.exec_())

## Run the application
if __name__ == '__main__':
    main()