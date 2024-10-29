# Imports
import queue
import time
import numpy as np
import pygame
import threading
from ParserClass import Parser
import LedController
import logging
logger = logging.getLogger(__name__)

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
    def __init__(self, parser : Parser):
        self.band = None
        self.intensity = None
        # self.frequency_queue = queue.Queue()
        self.currently_playing = False
        self.bpm = None
        self.stop_flag = False
        self.parser = parser
        self.led = LedController.LedControllerClass()
        pygame.mixer.init()
        self.update_led(operation=LedController.OperationType.ON)

    def close(self):
        logger.info("Closing Media...")
        self.parser.close()
        self.led.close()

    def update_led(self, operation : LedController.OperationType, blink_time=0):
        msg = LedController.Message(id=0, blink_time=blink_time, operation_type=operation)
        self.led.add_message(msg)

    def start_loop(self):
        self.listener_thread = threading.Thread(target=self.sound_loop)
        self.listener_thread.start()
        self.is_listening = True
        logger.info("Sound Loop started")

    def stop_loop(self):
        self.is_listening = False
        if self.listener_thread is not None:
            self.listener_thread.join()
            logger.debug("Sound Loop stopped")
    

    def sound_loop(self):
        for band, intensity in self.parser.get_detection():
            self.band = band
            self.intensity = intensity
            self.bpm = 30 + ((self.intensity / 100) * 300)
            self.update_led(operation=LedController.OperationType.BLINK, blink_time=0.5)
            # self.maps_to_bpm()
            metronome(self.bpm, DURATION)
            self.update_led(operation=LedController.OperationType.ON)

    def maps_to_bpm(self):
        self.bpm = ((self.intensity / 100) * 300)
        # if self.bpm != new_frequency:
        #     self.stop_flag = True
        #     self.bpm = new_frequency

        logger.debug(f"mapped intensity: {self.intensity} to bpm:{self.bpm}")

    def play_sound(self):
        while True:
            if self.bpm is not None and not self.currently_playing:
                self.stop_flag = False
                self.currently_playing = True
                start_time = time.time()

                while time.time() - start_time < 9:
                    if self.stop_flag:
                        break
                    if self.bpm == 500:
                        logger.debug(f"playing frequency: {self.bpm}")
                        metronome(self.bpm, 0.5)
                    else:
                        logger.debug(f"playing frequency: {self.bpm}")
                        metronome(self.bpm, 0.5)

                self.currently_playing = False
            else:
                logger.error('not entered')
            time.sleep(0.1)
