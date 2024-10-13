# Imports
import serial
import threading
from SenseiInputIFClass import SenseiInputIF


DEFAULT_COM_NUMBER = 5
DEFAULT_BAUD_RATE = 115200
BARKER= b'\xFE\xCA'
RX_BARKER= b'\xfe\xca'

class UARTInterface(SenseiInputIF):
    def __init__(self, port = f'COM{DEFAULT_COM_NUMBER}', baudrate=DEFAULT_BAUD_RATE, bytesize=8, parity='N', stopbits=1, timeout=1):
        self.serial_port = serial.Serial()
        self.serial_port.port = port
        self.serial_port.baudrate = baudrate
        self.serial_port.bytesize = bytesize
        self.serial_port.parity = parity
        self.serial_port.stopbits = stopbits
        self.serial_port.timeout = timeout
        self.is_listening = False
        self.listener_thread = None
        self.initialize()

    def initialize(self):
        if not self.serial_port.is_open:
            self.serial_port.open()
            print(f"UART initialized on {self.serial_port.port} with baudrate {self.serial_port.baudrate}")
            print(f"Bytesize: {self.serial_port.bytesize}, Parity: {self.serial_port.parity}, Stopbits: {self.serial_port.stopbits}")

    def setup(self, packet):
        if self.serial_port.is_open:
            self.serial_port.write(packet)
        else:
            print("Serial port is not open")
        print(f"Transmission Enabled setup message '{packet}' sent")

    def read_input(self):
        self.is_listening = True
        buffer = b''
        waiting_for_trigger = True

        while self.is_listening:
            if self.serial_port.in_waiting > 0:
                data = self.serial_port.read(self.serial_port.in_waiting)
                buffer += data

                if waiting_for_trigger:
                    if RX_BARKER in buffer:
                        waiting_for_trigger = False
                        buffer = buffer[buffer.index(RX_BARKER) + len(RX_BARKER):]
                        print(f"Trigger sequence detected: {BARKER}")

                while not waiting_for_trigger and len(buffer) >= 8:
                    chunk = buffer[:8]
                    buffer = buffer[8:]
                    print(chunk)
                    yield chunk
                    

    def start_listener(self):
        self.listener_thread = threading.Thread(target=self.read_input)
        self.listener_thread.start()
        print("Listener started")

    def stop_listener(self):
        self.is_listening = False
        if self.listener_thread is not None:
            self.listener_thread.join()
            print("Listener stopped")

    def close(self):
        if self.serial_port.is_open:
            self.serial_port.close()
            print(f"UART on {self.serial_port.port} closed")

# Example usage:
if __name__ == "__main__":
    uart = UARTInterface()
    uart.setup()
    #import pdb;pdb.set_trace()
    uart.start_listener()

    try:
        while True:
            pass  # Keep the main thread alive to listen to UART
    except KeyboardInterrupt:
        uart.stop_listener()
        uart.close()