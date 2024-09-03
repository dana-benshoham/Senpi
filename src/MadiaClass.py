# Imports
import queue
import time
import numpy as np
import pygame
from ParserClass import Parser

# Constants
FREQUENCY = 400
SAMPLE_RATE = 44100
DURATION_BEEP_MS = 100
VOLUME = 0.5
DURATION = 8


def metronome(bpm, duration):
    samples = np.sin(2 * np.pi * np.arange(SAMPLE_RATE * DURATION_BEEP_MS / 1000) * FREQUENCY / SAMPLE_RATE).astype(np.float32)
    samples = (VOLUME * 32767 * samples).astype(np.int16)
    stereo_samples = np.repeat(samples[:, np.newaxis], 2, axis=1)

    sound = pygame.sndarray.make_sound(stereo_samples)

    if bpm >= 300:
        end_time = time.time() + duration
        sound.play(-1)
        while time.time() < end_time:
            pass
        sound.stop()

    else:
        interval = (60.0 / bpm) - DURATION_BEEP_MS / 1000
        start_time = time.time()

        while (time.time() - start_time) < duration:
            sound.play()
            time.sleep(interval)
    # time.sleep(0.1)
    # pygame.mixer.quit()


class Media:
    def __init__(self, parser):
        self.band = None
        self.intensity = None
        # self.frequency_queue = queue.Queue()
        self.currently_playing = False
        self.bpm = None
        self.stop_flag = False
        self.parser = parser

        pygame.mixer.init()

    def sound_loop(self):
        for band, intensity in self.parser.get_detection():
            self.band = band
            self.intensity = intensity
            self.bpm = 30 + ((self.intensity / 100) * 300)
            # self.maps_to_bpm()
            metronome(self.bpm, DURATION)

    def maps_to_bpm(self):
        self.bpm = ((self.intensity / 100) * 300)
        # if self.bpm != new_frequency:
        #     self.stop_flag = True
        #     self.bpm = new_frequency

        print(self.bpm)

    def play_sound(self):
        while True:
            if self.bpm is not None and not self.currently_playing:
                self.stop_flag = False
                self.currently_playing = True
                start_time = time.time()
                print('test')

                while time.time() - start_time < 9:
                    if self.stop_flag:
                        break
                    if self.bpm == 500:
                        print(f"playing frequency: {self.bpm}")
                        metronome(self.bpm, 0.5)
                    else:
                        print(f"playing frequency: {self.bpm}")
                        metronome(self.bpm, 0.5)

                self.currently_playing = False
            else:
                print('not entered')
            time.sleep(0.1)
