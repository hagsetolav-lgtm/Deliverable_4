from functools import total_ordering
from math import gcd

@total_ordering
class Fraction:
    """Represent a fraction in its simplest form with a positive denominator."""


    def __init__(self, numerator: int, denominator: int) -> None:
        """Create  a fraction from to integers with positive denominator."""
        if type(numerator) is not int or type(denominator) is not int:
            raise TypeError("The numerator and denominator must be integers,")
        if denominator <= 0:
            raise ValueError("The denominator must be greater than zero.")

        divisor = gcd(numerator, denominator)
        self._numerator = numerator // divisor
        self._denominator = denominator // divisor


    @property
    def numerator(self) -> int:
        """Return the numerator of the simplified fraction."""
        return self._numerator


    @property
    def denominator(self) -> int:
        """Return the denominator of the simplified fraction."""
        return self._denominator


    def __eq__(self, other: object) -> bool:
        """Return whether two fractions have the same value."""
        if not isinstance(other, Fraction):
            return NotImplemented
        return (
            self.numerator == other.numerator
            and self.denominator == other.denominator
        )


    def __lt__(self, other: object) -> bool:
        """Return whether this fraction is smaller than the other fraction."""
        if not isinstance(other, Fraction):
            return NotImplemented
        return self.numerator * other.denominator < other.numerator * self.denominator


    def __add__(self, other: "Fraction") -> "Fraction":
        """Return the sum of two fractions."""
        if not isinstance(other, Fraction):
            return NotImplemented

        numerator = (
            self.numerator * other.denominator
            + other.numerator * self.denominator
        )
        denominator = self.denominator * other.denominator
        return Fraction(numerator, denominator)


    def __mul__(self, other: "Fraction") -> "Fraction":
        """Return the product of two fractions."""
        if not isinstance(other, Fraction):
            return NotImplemented

        numerator = self.numerator * other.numerator
        denominator = self.denominator * other.denominator
        return Fraction(numerator, denominator)


    def __str__(self) -> str:
        """Return the fraction in numerator/denominator form."""
        return f"{self.numerator}/{self.denominator}"


    def __repr__ (self) -> str:
        """Return a representation showing how to create the fraction."""
        return f"Fraction({self.numerator}, {self.denominator})"

