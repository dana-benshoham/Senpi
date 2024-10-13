import threading
import queue
import time
from dataclasses import dataclass
from enum import Enum
import RPi.GPIO as GPIO

LED_PIN = 17

class OperationType(Enum):
    ON = "On"
    OFF = "Off"
    BLINK = "Blink"

@dataclass
class Message:
    id: int
    blink_time: float
    operation_type: OperationType

class LedControllerClass:
    def __init__(self):
        self.message_queue = queue.Queue()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LED_PIN, GPIO.OUT)
        self.blink_time = 0
        self.blink_thread = threading.Thread(target=self._blink)
        self.blink_thread.daemon = True  # Allows the program to exit even if this thread is running
        self.blink_thread.start()

        self.fetcher_thread = threading.Thread(target=self._run)
        self.fetcher_thread.daemon = True  # Allows the program to exit even if this thread is running
        self.fetcher_thread.start()

    def operate_led(self, operation : OperationType, blink_time):
        self.blink_time = 0
        print(f"requested to {operation} with blink time {blink_time}")
        self.operation = operation
        self.blink_time = blink_time

    def _blink(self):
        self.is_blinking = True
        while self.is_blinking:
            if self.operation == OperationType.BLINK and self.blink_time != 0: 
                GPIO.output(LED_PIN, GPIO.HIGH)
                time.sleep(self.blink_time)
                GPIO.output(LED_PIN, GPIO.LOW)
                time.sleep(self.blink_time)
            elif self.operation == OperationType.ON:
                GPIO.output(LED_PIN, GPIO.HIGH)
            elif self.operation == OperationType.OFF:
                GPIO.output(LED_PIN, GPIO.LOW)
            elif self.operation == OperationType.None:
    

    def _run(self):
        self.is_running = True
        while self.is_running:
            try:
                # Try to get a message from the queue with a timeout
                message = self.message_queue.get(timeout=1)  # Wait for up to 1 second
                self.operate_led(message.operation_type, message.blink_time)
            except queue.Empty:
                if not self.is_running:
                    print("not running exiting...")
                    return 

    def add_message(self, message):
        self.message_queue.put(message)

    def stop(self):
        self.is_running = False
        self.is_blinking = False
        GPIO.cleanup()
        print("All messages have been processed.")

# Example usage
if __name__ == "__main__":
    led = LedControllerClass()
    blink_time = 0.5    # Simulate adding messages to the queue
    msg_type = OperationType.ON  
    msg = Message(id=0, blink_time=blink_time, operation_type=msg_type)
    led.add_message(msg)
    time.sleep(2)  # Simulate some delay in message arrival

    msg_type = OperationType.BLINK  
    msg = Message(id=1, blink_time=blink_time, operation_type=msg_type)
    led.add_message(msg)
    time.sleep(2)  # Simulate some delay in message arrival
    # Wait for all messages to be processed
    led.stop()