import contextlib
with contextlib.redirect_stdout(None):
    import pygame
    import edge_tts
    import asyncio
import os


def voice(text, file="play.mp3"):
    VOICES = ['en-US-GuyNeural', 'en-US-JennyNeural']
    TEXT = text
    VOICE = VOICES[0]
    OUTPUT_FILE = file

    async def amain():
        communicate = edge_tts.Communicate(TEXT, VOICE)
        await communicate.save(OUTPUT_FILE)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(amain())


def play(file="play.mp3"):
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def generate_voice(text):
    try:
        voice(text)
        play()
    except:
        pass

if __name__ == "__main__":
    generate_voice("In the golden light of morning, the butterflies of hope dance over the flower fields of dreams.")