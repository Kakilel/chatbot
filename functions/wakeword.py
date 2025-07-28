import queue
import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer

model = Model("models/vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)
audio_queue = queue.Queue()

wake_words = ["hey jarvis", "okay jarvis", "hello jarvis"]

def callback(indata, frames, time, status):
    if status:
        print("Stream status:", status)
    audio_queue.put(bytes(indata))

def detect_wake_word(callback):
    import speech_recognition as sr

    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)

    while True:
        with mic as source:
            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio).lower()
                if "fred" in text:  # Your wake word
                    callback()
            except sr.UnknownValueError:
                continue
            except Exception as e:
                print("Wake word error:", e)

