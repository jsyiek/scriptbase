import fractions
import math

from abc import abstractmethod
from typing import Union

class CompoundNumber:
    """
    Placeholder class for unsimplified numbers
    """
    def __init__(self, value = None):
        self.values = []
        self.compatible_types = []

    def __float__(self):
        """
        Needs to be implemented
        :return:
        """
        return


class BaseNumber:
    """
    Placeholder class for constants
    """

    def __init__(self, value: Union[float, fractions.Fraction], repr: str = None):
        self.value: Union[float, int, fractions.Fraction] = value
        self.repr: str = str(self.value)
        if repr is not None:
            self.repr = repr

    def __repr__(self):
        """
        This method should show what to print out as
        """
        return

    def __str__(self):
        return self.__repr__()

    def __float__(self):
        """
        This method should return the number's value when converting
        :return:
        """
        return self.value


class e:
    """
    Represents Euler's constant
    """