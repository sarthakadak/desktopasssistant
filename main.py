import os
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
from config import apikey

engine = pyttsx3.init()


def speak(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand. Please repeat.")
            return ""
        except sr.RequestError:
            print("Speech recognition service is unavailable.")
            return ""


genai.configure(api_key=apikey)


def chat_with_ai(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")  # Updated model name
        response = model.generate_content(prompt)
        if response and hasattr(response, 'candidates'):
            return response.candidates[0].content
        else:
            return "Sorry, I couldn't process the response."
    except Exception as e:
        print("Error:", e)
        return f"There was an error processing your request: {e}"


if __name__ == "__main__":
    print("Hey! I am Astra AI ")
    speak("Hey! I am Astra AI ")

    while True:
        user_input = take_command()
        if "exit" in user_input or "quit" in user_input:
            print("Goodbye!")
            speak("Goodbye!")
            break
        elif user_input:
            response = chat_with_ai(user_input)
            print("AI:", response)
            speak(response)
