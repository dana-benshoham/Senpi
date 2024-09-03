# Imports
from SenseiInputIFClass import SenseiInputIF


class Parser:
    def __init__(self, input_if: SenseiInputIF):
        self.input_if = input_if

    def get_detection(self):
        for packet in self.input_if.read_input():
            print(packet)
            packet = packet.strip()
            if ':' in packet:
                num1, num2 = packet.split(':')
                yield int(num1), int(num2)

