import fractions
import math

from typing import Iterator, Union


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

    @classmethod
    def from_mod_arg(cls,
                     modulus: Union[fractions.Fraction, float, int],
                     arg: Union[fractions.Fraction, float, int]) -> 'ComplexExI':
        """
        Assembles a ComplexExI object from modulus & argument; an alternative constructor

        Parameters:
            modulus (Union[fractions.Fraction, float, int]): Magnitude/modulus of the number
            arg (Union[fractions.Fraction, float, int]): Arg/theta of the number

        Returns:
            complex_number (ComplexExI): Complex number representation based on input info
        """
        return cls(real=modulus * math.cos(arg), imaginary=modulus * math.sin(arg))

    def __repr__(self) -> str:
        """
        Representation of the complex number. Displays as fraction.
        """
        return (f"{self.real}" if self.real or not self.imag else "") + (" + " if self.imag and self.real else "") \
               + (f"{self.imag}i" if self.imag else "")

    def __add__(self, other: Union[fractions.Fraction, float, int, complex, 'ComplexExI']) -> 'ComplexExI':
        """
        Adds two complex numbers together and returns a new object
        """
        if not (isinstance(other, ComplexExI) or isinstance(other, complex)):
            other = ComplexExI(other)
        return ComplexExI(real=self.real + other.real,
                          imaginary=self.imag + other.imag)

    def __sub__(self, other: Union[fractions.Fraction, float, int, complex, 'ComplexExI']) -> 'ComplexExI':
        """
        Subtracts two complex numbers together and returns a new object
        """
        return self.__add__(other * -1)

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
            ## If it's no complex, no further analysis necessary
            return ComplexExI(real=self.real/other,
                              imaginary=self.imag/other)
        elif isinstance(other, complex):
            other = ComplexExI(other.real, other.imag)

        return self.__mul__(other.inverse())

    def __pow__(self, other: Union[int, float, 'ComplexExI']) -> 'ComplexExI':
        """
        Raises the complex number to a power and returns a new object

        If you are taking a root, it's worth using the roots_of_unity method rather than explicitly using exponentiation
        """
        modulus = self.mag
        theta = self.arg
        if theta is None:
            ## to avoid type errors; if theta is None then modulus must be 0
            theta = 0

        ## other might be a complex number, so need to adjust the power to do that
        ## we can do this with some power math on the e
        ## also important that we keep track of the modulus here in the real category... e.g. k * e^(ix) = e^(ln(k) + ix)
        if isinstance(other, ComplexExI) or isinstance(other, complex):
            new_power = ComplexExI(real=math.log(modulus), imaginary=theta) * other
            modulus, theta = math.e ** new_power.real, new_power.imag
        else:
            ## Euler's formula
            theta, modulus = theta * other, modulus ** other
        return self.from_mod_arg(modulus=modulus, arg=theta)

    @property
    def arg(self) -> Union[float, None]:
        """
        Returns the argument of the complex number, or None if the arg isn't defined

        Returns:
            arg (Union[float, None]): Floating point number representing the arg of the complex number
                                      (None if the arg isn't defined - i.e. self.real = 0 and self.imag = 0
        """
        if self.real == 0:
            if self.imag == 0:
                return None
            else:
                return 1 if self.imag > 0 else -1
        elif self.real > 0:
            ## quads 1 and 4 has arctan compatibility
            return math.atan(self.imag/self.real)
        elif self.real < 0 and self.imag >= 0:
            ## If in quad 2 we can use acos because it has range over that
            return math.acos(self.real/self.mag)
        else:
            ## this is the oddball case of quad 3
            return math.acos(self.imag/self.real) - math.pi

    @property
    def conj(self) -> 'ComplexExI':
        """
        Creates a new complex object that represents the conjugate of this complex #

        Returns:
            conjugate (ComplexExI): New Complex obj representing the conj of the current one
        """
        return ComplexExI(real=self.real,
                          imaginary=-1 * self.imag)

    @property
    def mag(self) -> float:
        """
        Calculates the magnitude of the complex number

        Returns:
            magnitude (float): Magnitude of the complex number
        """
        return (self.real ** 2 + self.imag ** 2) ** 0.5

    def as_float_string(self, decimal_places: Union[int, float] = None) -> str:
        """
        Returns a string representing the complex number as a float

        Parameters:
            decimal_places (Union[int, float]): Number of DP to round to

        Returns:
            float_str (str): the same as __repr__ but with floats instead of fractions
        """
        if decimal_places is None:
            return (f"{float(self.real)}" if self.real or not self.imag else "") \
                   + (" + " if self.imag and self.real else "") \
                   + (f"{float(self.imag)}i" if self.imag else "")
        else:
            return (f"{round(float(self.real), decimal_places)}" if self.real or not self.imag else "") \
                   + (" + " if self.imag and self.real else "") \
                   + (f"{round(float(self.imag), decimal_places)}i" if self.imag else "")

    def inverse(self) -> 'ComplexExI':
        """
        Returns a new complex object representing 1 over this object

        Returns:
            inverse (ComplexExI): New Complex obj representing inverse of the current one
        """
        denominator = self.real ** 2 - self.imag ** 2
        return self.conj/denominator

    def roots_of_unity(self, n: Union[int, float, fractions.Fraction]) -> Iterator['ComplexExI']:
        """
        Calculates the nth roots of unity.

        Parameters:
            n (Union[int, float, fractions.Fraction]): The nth roots of unity to find, equivalent to C ** (1/n)

        Yields:
            Roots of Unity ('ComplexExI')

        Returns:
            None
        """

        rationalized = fractions.Fraction(n)

        ## raise to the denominator (remember n is the n from 1/n, so the num/denom are flipped)
        new_number = self ** rationalized.denominator

        ## We only need the numerator
        n = rationalized.numerator
        modulus = new_number.mag ** (1/n)
        new_num_arg_over_n = new_number.arg / n

        i = 0
        while i != n:

            arg = new_num_arg_over_n + 2 * math.pi * (i + 1) / n
            yield new_number.from_mod_arg(modulus, arg)

            i += 1


## Tests
comp_one = ComplexExI(3, 2)
comp_two = ComplexExI(-1, 4)
comp_three = ComplexExI(1, 0)
comp_exp = comp_three.roots_of_unity(1024)
for res in comp_exp:
    print(res.as_float_string(5))
