# Imports
import time

from SenseiInputIFClass import SenseiInputIF
from FileIFClass import FileIF
from ParserClass import Parser
from MadiaClass import Media
import threading


# Constants
FILE_TESTS = r"../tests"


def main():
    input_if = FileIF(FILE_TESTS)
    parser_input = Parser(input_if)

    media = Media(parser_input)

    media.sound_loop()


if __name__ == '__main__':
    main()
