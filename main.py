# import pygame
import os
from audio import main_audio_loop, pedal_loop
import colorama
from beans_frontend import *
import sys
import pyaudio
import whisper
colorama.init()

if __name__ == "__main__":
    """
    Main function call to start Beans

    IMPORTANT: KEYS.py
    In order for Beans to properly function, you must create a file titled KEYS.py
    In this file, you must place the following:
        elabs_api = [
            '{elabs api #1}',
            '{elabs api #2}', and so on
        ]
        voice_api = [
            '{elabs voice api #1}',
            '{elabs voice api #2}', and so on
        ]
        gpt_key = '{GPT key from OpenAI}'
        user_name = '{Your name}
        GOOGLE_DEV_API = '{Your Google Dev API, optional}'
        SEARCH_ENGINE_ID = '{Your Google Search Engine ID, optional}'
        SPOTIPY_CLIENT_ID = '{Your Spotipy client ID, optional but may crash}'
        SPOTIPY_CLIENT_SECRET = '{Your Spotipy client secret, optional but may crash}'
        SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback' or whatever else you want to specify
    """
    pedal = True
    for arg in sys.argv:
        if '--nopedal' in arg:
            pedal = False
    pyaudio_instance = pyaudio.PyAudio()
    model = whisper.load_model("tiny")

    # Main loop
    # This mainly is for TTS and STT, but more functions can be added
    show_image_in_bottom_right(os.path.join('art','bird_closed_mouth.png'))
    while True:
        if pedal:
            pedal_loop(pyaudio_instance=pyaudio_instance, model=model)
        else:
            main_audio_loop(pyaudio_instance=pyaudio_instance, model=model)