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

@pytest.mark.parameterize("invalid_unit", ["X", "", "Celsius"])
def test_invalid_units(invalid_unit: str) -> None:
    """Reject invalid unit strings during creation and conversion."""
    with pytest.raises(ValueError):
        Temperature(10, invalid_unit)

    temperature = Temperature(10, "C")
    with pytest.raises(ValueError):
        temperature.convert_to(invalid_unit)

@pytest.mark.parameterize(
    "value, unit",
    [(-273.16, "C"), (-459.68, "F"), (-0.01, "K")],
)
def test_below_absolute_zero(value: float, unit: str) -> None:
    """Reject temperatures below absolute zero for each unit."""
    with pytest.raises(ValueError):
        Temperature(value, unit)


# 3. Conversions at the five reference points.

@pytest.mark.parameterize("startin_unit", ["C", "F", "K"])
@pytest.mark.parameterize(
    "celsius", "fahrenheit", "kelvin",
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
