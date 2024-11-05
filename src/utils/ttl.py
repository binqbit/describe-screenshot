import os
import threading
import uuid
from gtts import gTTS
import numpy as np
import librosa
import soundfile as sf
import pygame

LANGUAGE = os.getenv("LANGUAGE", "en")

def text_to_audio(text, filename):
    tts = gTTS(text=text, lang=LANGUAGE)
    tts.save(filename)

def play_audio(filename):
    data, samplerate = librosa.load(filename, sr=None)
    faster_data = librosa.effects.time_stretch(data, rate=1.5)
    faster_data = np.int16(faster_data * 50000)
    sf.write(filename, faster_data, samplerate)
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()

def play_text(text, path, is_wait = True):
    def play_text_thread(text, path):
        filename = f"{path}/file_{uuid.uuid4()}.mp3"
        try:
            text_to_audio(text, filename)
            play_audio(filename)
        except Exception as e:
            print("Play text error:", e)
        os.remove(filename)
    if is_wait:
        play_text_thread(text, path)
    else:
        threading.Thread(target=play_text_thread, args=(text, path)).start()