"""Test the Temperature class with pytest."""

import pytest
from temperature import Temperature

# 1. Initialization.

def test_default_unit() -> None:
    """Use Celsius when no unit is applied."""
    temperature = Temperature(25)

    assert temperature.value == 25.0
    assert temperature.unit == "C"

@pytest.mark.parametrize("unit", ["c", "C", "f", "F", "k", "K"])
def test_case_insensitive_units(unit: str) -> None:
    """Accept both uppercase and lowercase symbols."""
    temperature = Temperature(10, unit)

    assert temperature.unit == unit.upper()
    assert temperature.value == 10.0

def test_read_only_attributes() -> None:
    """Raise AttributeError when the value or unit is reassigned."""
    temperature = Temperature(20, "C")

    with pytest.raises(AttributeError):
        temperature.value = 30

    with pytest.raises(AttributeError):
        temperature.unit = "F"


# 2. Validation.

@pytest.mark.parametrize("invalid_unit", ["X", "", "Celsius"])
def test_invalid_units(invalid_unit: str) -> None:
    """Reject invalid unit strings during creation and conversion."""
    with pytest.raises(ValueError):
        Temperature(10, invalid_unit)

    temperature = Temperature(10, "C")
    with pytest.raises(ValueError):
        temperature.convert_to(invalid_unit)

@pytest.mark.parametrize(
    "value, unit",
    [(-273.16, "C"), (-459.68, "F"), (-0.01, "K")],
)
def test_below_absolute_zero(value: float, unit: str) -> None:
    """Reject temperatures below absolute zero for each unit."""
    with pytest.raises(ValueError):
        Temperature(value, unit)


# 3. Conversions at the five reference points.

@pytest.mark.parametrize("starting_unit", ["C", "F", "K"])
@pytest.mark.parametrize(
    "celsius, fahrenheit, kelvin",
    [
        (-273.15, -459.67, 0.0),
        (-40.0, -40.0, 233.15),
        (0.0, 32.0, 273.15),
        (37.0, 98.6, 310.15),
        (100.0, 212.0, 373.15),
    ],
    ids=["absolute_zero", "crossover", "freezing", "body", "boiling"],
)
def test_reference_conversions(
    starting_unit: str, celsius: float, fahrenheit: float, kelvin: float
) -> None:
    """Convert each reference temperature from every possible starting unit."""
    values = {"C": celsius, "F": fahrenheit, "K": kelvin}
    temperature = Temperature(values[starting_unit], starting_unit)

    assert temperature.to_celsius() == pytest.approx(celsius, abs=1e-9)
    assert temperature.to_fahrenheit() == pytest.approx(fahrenheit, abs=1e-9)
    assert temperature.to_kelvin() == pytest.approx(kelvin, abs=1e-9)

# 4. Round-trip conversion.

def test_round_trip() -> None:
    """Convert C to F to K to C and recover original temperature."""
    original = Temperature(21.5, "C")
    fahrenheit = original.convert_to("f")
    kelvin = fahrenheit.convert_to("k")
    result = kelvin.convert_to("c")

    assert (fahrenheit.unit, kelvin.unit, result.unit) == ("F", "K", "C")
    assert result.value == pytest.approx(21.5, abs=1e-9)
    assert result == original
    assert result is not original
    assert original.unit == "C"

def test_cross_unit_comparisons() -> None:
    """Check equality and ordering for equal/unequal temperatures."""
    freezing = Temperature(0, "C")
    equivalent = Temperature(32, "F")
    warmer = Temperature(300, "K")

    assert freezing == equivalent
    assert freezing <= equivalent
    assert freezing >= equivalent
    assert not (freezing < equivalent)
    assert not (freezing > equivalent)

    assert freezing != warmer
    assert freezing < warmer
    assert freezing <= warmer
    assert warmer > equivalent
    assert warmer >= equivalent

def test_comparison_tolerance() -> None:
    """Treat differences within 1e-9K as equal."""
    baseline = Temperature(10, "K")
    assert baseline == Temperature(10 + 0.5e-9, "K")
    assert baseline < Temperature(10 + 2e-9, "K")

def test_string_formatting() -> None:
    """Check exact human-readable and developer representations."""
    temperature = Temperature(25, "C")

    assert str(temperature) == "25.00 °C"
    assert repr(temperature) == "Temperature(25.0, 'C')"