import pyttsx3
import speech_recognition as sr

from conv import random_text
from random import choice
from datetime import datetime
from decouple import config

engine = pyttsx3.init('sapi5')
engine.setProperty('volume', 1.5)
engine.setProperty('rate', 225)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

USER = config('USER')
HOSTNAME = config('BOT')


def speak(text):
    engine.say(text)
    engine.runAndWait()


def greetMe():
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good Morning {USER}")
    elif (hour >= 12) and (hour < 16):
        speak(f"Good Afternoon {USER}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Good Evening {USER}")
    speak(f"I am {HOSTNAME}. How can I assist you {USER}?")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        queri = r.recognize_google_cloud(audio, language='en=in')
        print(queri)
        if not 'stop' in queri or 'exit' in queri:
            speak(choice(random_text))
        else:
            hour = datetime.now().hour
            if (hour >= 21) and (hour < 6):
                speak(f"Good Night {USER}, Take Care !")
            else:
                speak(f"Have a good day, {USER}!")
            exit()

    except Exception:
        speak("Sorry, I couldn't understand. Can you please repeat what you just said?")
        queri = 'None'
    return queri


if __name__ == '__main__':
    greetMe()
    while True:
        query = takeCommand().lower()
        if "how are you" in query:
            speak("I am absolutely fine. What about you ?")
