import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import random
from gtts import gTTS
import pygame
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def get_weather(city):
    api_key = "your_openweathermap_api_key"  # Replace with a valid API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    if response.get("main"):
        temp = response["main"]["temp"]
        description = response["weather"][0]["description"]
        return f"The temperature in {city} is {temp}°C with {description}."
    else:
        return "I couldn't get the weather. Please check the city name."

def get_random_fact():
    facts = [
        "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3000 years old and still perfectly good.",
        "Bananas are berries, but strawberries aren't.",
        "A day on Venus is longer than a year on Venus.",
        "Octopuses have three hearts.",
        "Sharks existed before trees."
    ]
    return random.choice(facts)

def get_motivation():
    quotes = [
        "Believe in yourself and all that you are.",
        "The only way to do great work is to love what you do.",
        "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "Don't watch the clock; do what it does. Keep going.",
        "Difficulties in life are intended to make us better, not bitter."
    ]
    return random.choice(quotes)

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")  
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music.get(song, None)
        if link:
            webbrowser.open(link)
        else:
            speak(f"Sorry, I couldn't find {song}. You can add it to the library.")
    elif "weather in" in c.lower():
        city = c.lower().split("weather in ")[1]
        speak(get_weather(city))
    elif "tell me a fact" in c.lower():
        speak(get_random_fact())
    elif "motivate me" in c.lower():
        speak(get_motivation())

if __name__ == "__main__":
    speak("Initializing Cheetah....")
    while True:
        r = sr.Recognizer()
        
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if word.lower() == "cheetah":
                speak("Yes?")
                with sr.Microphone() as source:
                    print("Cheetah Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processCommand(command)
        except Exception as e:
            print("Error: {0}".format(e))
    

