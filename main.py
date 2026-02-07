import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import random
from gtts import gTTS
import pygame
import os
import time

recognizer = sr.Recognizer()
engine = pyttsx3.init()

# ---------- TEXT TO SPEECH ----------

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    try:
        tts = gTTS(text)
        filename = "temp.mp3"
        tts.save(filename)

        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.music.unload()
        pygame.mixer.quit()

        if os.path.exists(filename):
            os.remove(filename)

    except Exception:
        speak_old(text)

# ---------- FEATURES ----------

def get_weather(city):
    api_key = "YOUR_API_KEY_HERE"  # replace with real key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()

    if response.get("main"):
        temp = response["main"]["temp"]
        description = response["weather"][0]["description"]
        return f"The temperature in {city} is {temp} degree Celsius with {description}."
    else:
        return "Sorry, I couldn't fetch the weather."

def get_random_fact():
    facts = [
        "Honey never spoils.",
        "Bananas are berries, but strawberries are not.",
        "A day on Venus is longer than a year on Venus.",
        "Octopuses have three hearts.",
        "Sharks existed before trees."
    ]
    return random.choice(facts)

def get_motivation():
    quotes = [
        "Believe in yourself.",
        "Do what you love and love what you do.",
        "Failure is not the opposite of success, it is part of success.",
        "Keep going. Everything you need will come to you.",
        "Dream big and dare to fail."
    ]
    return random.choice(quotes)

# ---------- COMMAND PROCESSING ----------

def processCommand(command):
    command = command.lower()

    if "open google" in command:
        webbrowser.open("https://google.com")

    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")

    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in command:
        webbrowser.open("https://linkedin.com")

    elif command.startswith("play"):
        song = command.replace("play", "").strip()
        link = musicLibrary.music.get(song)

        if link:
            speak(f"Playing {song}")
            webbrowser.open(link)
        else:
            speak("Sorry, I couldn't find that song.")

    elif "weather in" in command:
        city = command.split("weather in")[-1].strip()
        speak(get_weather(city))

    elif "tell me a fact" in command:
        speak(get_random_fact())

    elif "motivate me" in command:
        speak(get_motivation())

    elif "exit" in command or "stop" in command or "quit" in command:
        speak("Goodbye! See you soon.")
        exit()

    else:
        speak("Sorry, I didn't understand that.")

# ---------- MAIN LOOP ----------

if __name__ == "__main__":
    speak("Initializing Cheetah")

    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)

            wake_word = recognizer.recognize_google(audio).lower()

            if wake_word == "cheetah":
                speak("Yes?")
                with sr.Microphone() as source:
                    print("Cheetah active...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    command = recognizer.recognize_google(audio)
                    processCommand(command)

        except sr.UnknownValueError:
            pass  # ignore noise

        except sr.WaitTimeoutError:
            pass  # user silent

        except Exception as e:
            print("Error:", e)
