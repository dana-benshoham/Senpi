# Imports
import time

from SenseiInputIFClass import SenseiInputIF
from FileIFClass import FileIF
from SerialIFClass import UARTInterface
from ParserClass import Parser
from MadiaClass import Media
from DetectorClass import Detector
import LedController
import json
import threading
import logging
import logging.handlers

# Configure the root logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.handlers.TimedRotatingFileHandler('app.log', when='midnight', interval=1, backupCount=7),
                        logging.StreamHandler()
                    ])

# Constants
FILE_TESTS = r"../tests"

def log_level_string_to_enum(level):
    if level=='DEBUG':
        return logging.DEBUG
    elif level == 'INFO':
        return logging.INFO
    elif level == 'WARNING':
        return logging.WARNING
    elif level == 'ERROR':
        return logging.ERROR
    elif level == 'FATAL':
        return logging.FATAL
    elif level == 'CRITICAL':
        return logging.CRITICAL

def default_initialize():
    input_if = UARTInterface()

    parser_input = Parser(input_if)

    led_control = LedController.LedControllerClass()

    return Media(parser=parser_input, led_control=led_control)

def initialize(config):
    if config['interface']['type']=='UART':
        uart_config = config['interface']['config']
        input_if = UARTInterface(baudrate=uart_config['baudrate'], \
                                 port=uart_config['port'], \
                                 stopbits=uart_config['stopbits'], \
                                 timeout=uart_config['timeout'], \
                                 bytesize=uart_config['bytesize'], \
                                 parity=uart_config['parity'], \
                                 log_level=log_level_string_to_enum(config['interface']['log_level']))
                                        
    else:
        input_if = FileIF(FILE_TESTS)

    parser_input = Parser(input_if=input_if, log_level=config['parser']['log_level'])

    detector = Detector(parser=parser_input, log_level=config['detector']['log_level'])

    led_control = LedController.LedControllerClass(led_pin=config['led_controller']['pin'],\
                                                   log_level=log_level_string_to_enum(config['led_controller']['log_level']))

    return Media(detector=detector, led_control=led_control, log_level=log_level_string_to_enum(config['media']['log_level']))


def main():
    config = {}
    with open("config.json") as f_in:
        config = json.load(f_in)

    if config == {}:
        media = default_initialize()
    else:
        media = initialize(config)
    
    media.start_loop()

    try:
        while True:
            pass  # Keep the main thread alive 
    except KeyboardInterrupt:
        media.close()

if __name__ == '__main__':
    main()
