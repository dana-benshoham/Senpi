# Imports
import os
import time
from os import listdir
from os.path import isfile, join

from SenseiInputIFClass import SenseiInputIF


class FileIF(SenseiInputIF):
    def __init__(self, file_path):
        self.file_path = f"{os.path.dirname(os.path.realpath(__file__))}/{file_path}"
        self.sleep_suite = 30
        self.sleep_after_test = 2

    def read_input(self):
        while True:
            test_files = [f for f in listdir(self.file_path) if isfile(join(self.file_path, f))]
            for file in test_files:
                with open(f"{self.file_path}/{file}", 'r') as file_input:
                    for line in file_input:
                        yield line
                print(f"test {file} finished succesfully, sleeping for {self.sleep_after_test} seconds")
                time.sleep(self.sleep_after_test)
            print(f"all files in {self.file_path} ran succesfully, sleeping for {self.sleep_suite} seconds")
            time.sleep(self.sleep_suite)
