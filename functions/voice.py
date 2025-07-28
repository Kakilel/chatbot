import speech_recognition as sr
import pyttsx3


engine = pyttsx3.init()
engine.setProperty("rate", 180)  
engine.setProperty("voice", engine.getProperty("voices")[1].id)  

def speak(text: str):
    """Speak the given text out loud."""
    engine.say(text)
    engine.runAndWait()

def listen(timeout=5, phrase_time_limit=10):
    """Listen to the microphone and return the transcribed text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.WaitTimeoutError:
            print("Timeout: No speech detected.")
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print(f"Speech Recognition error: {e}")
    return ""
