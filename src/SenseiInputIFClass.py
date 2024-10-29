# Imports
from abc import ABC, abstractmethod

class SenseiInputIF(ABC):
    @abstractmethod
    def read_input(self):
        pass

    @abstractmethod
    def setup(self, packet):
        pass

    @abstractmethod
    def close(self):
        pass