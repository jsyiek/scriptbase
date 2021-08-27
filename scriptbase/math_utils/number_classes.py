import fractions
import math


class Complex:
    """
    Represents a complex number (a + bi)
    """

    def __init__(self, real: fractions.Fraction, imaginary: fractions.Fraction):
        """
        Parameters:
            real (fractions.Fraction): Real portion of the complex number
            imaginary (fractions.Fraction): Imaginary portion, without trailing i
        """

        ## Store in modulus argument form, but store the args as a tangent
        ## i.e. k * (cos(x) + i*sin(x))
        self.modulus = math.sqrt(real**2 + imaginary**2)
        self.cos = real/self.modulus
        self.sin = imaginary/self.modulus

        ## Doesn't hurt to save the input values
        self.real = real
        self.imaginary = imaginary


