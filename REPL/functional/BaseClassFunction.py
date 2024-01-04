from abc import ABC, abstractmethod


class GreenFunction(ABC):
    def __init__(self):
        pass

    @staticmethod
    @abstractmethod
    def run(*args):
        pass


class RedFunction(GreenFunction, ABC):
    @staticmethod
    @abstractmethod
    def get_confirmation_message(*args):
        pass
