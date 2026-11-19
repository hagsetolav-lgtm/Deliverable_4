from functools import total_ordering
from math import isclose

@total_ordering
class Temperature:
    """Represent a temperature in Celsius, Fahrenheit, or Kelvin."""

    _TOLERANCE = 1e-9
    _ABSOLUTE_ZERO = {"C": -273.15, "F": -459.67, "K": 0.0}

    def __init__(self, value: float, unit: str = "C") -> None:
        """Create  a temperature, raise ValueError for invalid unit og value"""
        self._unit = self._validate_unit(unit)
        self._value = float(value)

        if self._value < self._ABSOLUTE_ZERO[self._unit]:
            raise ValueError("Temperature cannot be below absolute zero.")

    @staticmethod
    def _validate_unit(unit: str) -> str:
        """Return the uppercase unit or ValueError if the unit is invalid."""
        if not isinstance(unit, str) or unit.upper() not in ("C", "F", "K"):
            raise ValueError("Unit must be 'C', 'F' or 'K'.")
        return unit.upper()

    @property
    def value(self) -> float:
        """Return the temperature value in its original unit."""
        return self._value

    @property
    def unit(self) -> str:
        """Return the uppercase unit symbol."""
        return self._unit

    def to_celsius(self) -> float:
        """Return the temperature in Celsius."""
        if self.unit == "F":
            return (self.value-32) * 5/9
        if self.unit == "K":
            return self.value - 273.15
        return self.value

    def to_fahrenheit(self) -> float:
        """Return the temperature in Fahrenheit."""
        if self.unit == "F":
            return self.value
        return self.to_celsius() * 9/5 + 32

    def to_kelvin(self) -> float:
        """Return the temperature in Kelvin."""
        if self.unit == "K":
            return self.value
        if self.value == self._ABSOLUTE_ZERO[self.unit]:
            return 0.0
        return self.to_celsius() + 273.15

    def convert_to(self, target_unit: str) -> "Temperature":
        """Return a new Temperature expressed in the requested unit."""
        unit = self._validate_unit(target_unit)
        if unit == "C":
            value = self.to_celsius()
        elif unit == "F":
            value = self.to_fahrenheit()
        else:
            value = self.to_kelvin()

        # At absolute zero, use the exact boundary as the target unit.
        if self.value == self._ABSOLUTE_ZERO[self.unit]:
            value = self._ABSOLUTE_ZERO[unit]
        return Temperature(value, unit)

    def __repr__(self) -> str:
        """Return a string representation of the temperature."""
        return f"Temperature({self.value!r}, {self.unit!r})"

    def __str__(self) -> str:
        """Return the temperature formatted to two decimal places."""
        symbol = "K" if self.unit == "K" else f"°{self.unit}"
        return f"{self.value:.2f} {symbol}"

    def __eq__(self, other: object) -> bool:
        """Return whether temperatures agree with the absolute tolerance."""
        if not isinstance(other, Temperature):
            return NotImplemented
        return isclose(
            self.to_kelvin(),
            other.to_kelvin(),
            rel_tol=0.0,
            abs_tol=self._TOLERANCE,
        )

    def __lt__(self, other: object) -> bool:
        """Return whether the temperature is colder by more than the tolerance."""
        if not isinstance(other, Temperature):
            return NotImplemented
        return self != other and self.to_kelvin() < other.to_kelvin()
