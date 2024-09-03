# Imports
import serial
import threading
from SenseiInputIFClass import SenseiInputIF


class SerialIF(SenseiInputIF):
    def __init__(self, port='COM3', baudrate=9600, timeout=1, ):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_conn = None
        self.running = False
        self.dict = {'read_nco': 'aaa'}
        self.wait_time=1

    def start(self):
        if self.serial_conn is None:
            self.serial_conn = serial.Serial(
                self.port,
                self.baudrate,
                timeout=self.timeout
            )
        self.running = True

    def stop(self):
        self.running = False
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()

    def send_packet(self):
        self.serial_conn.write(self.dict['read_nco'])

    def receive_response(self):
        try:
            while self.running:
                if self.serial_conn.in_waiting > 6:
                    string_input_if = self.serial_conn.read(7)
                    yield string_input_if
        finally:
            self.stop()

    def read_input(self):
        self.start()
        while self.running:
            self.send_packet()
            print(f'Packet sent: {self.dict['read_nco']}')
            self.receive_response()



