# Imports
import time

from SenseiInputIFClass import SenseiInputIF
from FileIFClass import FileIF
# from SerialIFClass import UARTInterface
from ParserClass import Parser
from MadiaClass import Media
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


def main():
    input_if = FileIF(FILE_TESTS)
    # input_if = UARTInterface()

    parser_input = Parser(input_if)

    media = Media(parser_input)

    media.sound_loop()


if __name__ == '__main__':
    main()
