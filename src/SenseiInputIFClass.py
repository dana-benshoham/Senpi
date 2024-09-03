# Imports
from abc import ABC, abstractmethod


class SenseiInputIF(ABC):
    @abstractmethod
    def read_input(self):
        pass
