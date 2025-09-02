import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from gtts import gTTS
import pygame
import os
import requests

MISTRAL_API_KEY = "TbnLdpjspg7M6iik9MYC6z73p2AkUOo0"  # Replace with your actual key
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"



recognizer = sr.Recognizer()
engine = pyttsx3.init() 
engine.setProperty('rate', 160)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) 
newsapi = "00190428b26b482ebfd2d5c783073ce2"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 

def aiProcessMistral(command):
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistral-large-latest",
        "messages": [
            {"role": "system", "content": "You are Julie, a helpful voice assistant. Keep responses short and clear."},
            {"role": "user", "content": command}
        ]
    }

    response = requests.post(MISTRAL_API_URL, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print("Mistral error:", response.text)
        return "Sorry, I couldn't process that right now."

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
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])

    else:
        # Let OpenAI handle the request
        output = aiProcessMistral(c)
        speak(output) 





if __name__ == "__main__":
    speak("Initializing Julie....")
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
         
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source)
            word = r.recognize_google(audio)
            if(word.lower() == "julie"):
                speak("Ya")
                # Listen for command
                with sr.Microphone() as source:
                    print("Julie Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)


        except Exception as e:
            print("Error; {0}".format(e))
