from abc import abstractmethod
from abc import ABCMeta

class I_Normalize(metaclass=ABCMeta):

    @abstractmethod
    def normalize(self, elems:list):
        pass