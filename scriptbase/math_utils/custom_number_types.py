import fractions
import math

from typing import Union


class ComplexExI:
    """
    Represents a complex number (a + bi) using real & imaginary
    """

    def __init__(self,
                 real: Union[fractions.Fraction, float, int] = 0,
                 imaginary: Union[fractions.Fraction, float, int] = 0):
        """
        Parameters:
            real (fractions.Fraction): Real portion of the complex number
            imaginary (fractions.Fraction): Imaginary portion, without trailing i
        """

        self.real = fractions.Fraction(real)
        self.imag = fractions.Fraction(imaginary)

    def __repr__(self):
        return f"{self.real}" if self.real or not self.imag else "" + f"{self.imag}i" if imag else ""

    def __add__(self, other: Union[fractions.Fraction, float, int, complex, 'ComplexExI']) -> 'ComplexExI':
        """
        Adds two complex numbers together and returns a new object
        """
        if not (isinstance(other, ComplexExI) or isinstance(other, complex)):
            other = ComplexExI(other)
        return ComplexExI(real=self.real + other.real,
                          imaginary=self.imag + other.imag)

    def __mul__(self, other: Union[fractions.Fraction, float, int, complex, 'ComplexExI']) -> 'ComplexExI':
        """
        Multiplies two complex numbers and returns a new object
        """
        if not (isinstance(other, ComplexExI) or isinstance(other, complex)):
            other = ComplexExI(other)
        return ComplexExI(real=self.real * other.real - self.imag * other.imag,
                          imaginary=self.real * other.imag + other.real * self.imag)

    def __truediv__(self, other: Union[fractions.Fraction, float, int, complex, 'ComplexExI']) -> 'ComplexExI':
        """
        Divides two complex numbers and returns a new object
        """
        if not (isinstance(other, ComplexExI) or isinstance(other, complex)):
            other = ComplexExI(other)
        elif isinstance(other, complex):
            other = ComplexExI(other.real, other.imag)

        return self.__mul__(other.inverse())

    def __pow__(self, other: Union[int, float]):
        """
        Raises the complex number to a power and returns a new object
        """
        modulus = (self.real ** 2 + self.imag ** 2) ** 0.5
        if self.real >= 0:
            ## qquads 1 and 4 has arctan compatibility
            theta = math.atan(self.imag/self.real)
        elif self.real <= 0 and self.imag >= 0:
            ## If in quad 2 we can use acos because it has range over that
            theta = math.acos(self.real/modulus)
        else:
            ## this is the oddball case of quad 3
            theta = math.acos(self.imag/self.real) - math.pi

        ## Euler's formula
        theta, modulus = theta * other, modulus ** other
        return ComplexExI(real=modulus * math.cos(theta),
                          imaginary=modulus * math.sin(theta))

    def conj(self) -> 'ComplexExI':
        """
        Returns a new complex object that represents the conjugate of this complex #

        Returns:
            conjugate (Complex): New Complex obj representing the conj of the current one
        """
        return ComplexExI(real=self.real,
                          imaginary=-1 * self.imag)

    def inverse(self) -> 'ComplexExI':
        """
        Returns a new complex object representing 1 over this object

        Returns:
            inverse (Complex): New Complex obj representing inverse of the current one
        """
        denominator = self.real ** 2 - self.imag ** 2
        return self.conj()/denominator

## Tests
comp_one = ComplexExI(3, 2)
comp_exp = comp_one ** 3
print(comp_exp)
