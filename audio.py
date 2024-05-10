import pyaudio
import wave
import threading
import whisper
from convo_processing import get_response, process_convo
import requests
from KEYS import elabs_api, voice_api
import pygame
import os

pygame.init() # TODO: move this to main.py

def record_audio(model, duration=10, rate=44100, chunk=1024, channels=2, format=pyaudio.paInt16):
    p = pyaudio.PyAudio()
    print("Recoding audio...")
    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    frames = []

    for i in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Saving audio...")

    wf = wave.open("recording.wav", 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()
    print("record_audio complete.\n")


def main_audio_loop():
    model = whisper.load_model("medium")

    while True:
        record_audio(model)
        convo = model.transcribe("recording.wav", verbose=False, language='en', fp16=False)['text'].lower()
        print(convo)
        if 'pluto' in convo:
            print("Name heard!")
            # while convo:
            tag = process_convo(convo)
            response = get_response(tag) 
            speak(response) #TODO: update this to allow conversations

def speak(response):
    print("Speaking...")
    CHUNK_SIZE = 1024
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_api}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": f"{elabs_api}"
    }

    data = {
        "text": response,
        "model_id": "eleven_turbo_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
    }
    }

    response = requests.post(url, json=data, headers=headers)
    with open('output.mp3', 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
    pygame.mixer.Sound('output.mp3').play()