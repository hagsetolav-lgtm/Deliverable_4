"""Test the Fraction class with pytest."""

import pytest
from fraction import Fraction

@pytest.mark.parametrize(
    "numerator, denominator, expected_numerator, expected_denominator",
    [
        (3, 5, 3, 5),
        (6, 8, 3, 4),
        (-6, 8, -3, 4),
        (0, 7, 0, 1),
    ]
)
def test_initialization(
    numerator: int,
    denominator: int,
    expected_numerator: int,
    expected_denominator: int,
) -> None:
    """Store positive, negative and zero fractions in the easiest form."""
    fraction = Fraction(numerator, denominator)

    assert fraction.numerator == expected_numerator
    assert fraction._denominator == expected_denominator


@pytest.mark.parametrize("invalid_value", [1.5, "2", True])
def test_integer_inputs_required(invalid_value: object) -> None:
    """Reject non-integer inputs in either position, including booleans."""
    with pytest.raises(TypeError):
        Fraction(invalid_value, 2)
    with pytest.raises(TypeError):
        Fraction(1, invalid_value)


@pytest.mark.parametrize("denominator", [0, -3])
def test_denominator_must_be_positive(denominator: int) -> None:
    """Reject zero and negative denominators."""
    with pytest.raises(ValueError):
        Fraction(1, denominator)


def test_equivalent_fractions() -> None:
    """Compare equal values written with different denominators."""
    half = Fraction(1, 2)
    two_quarters = Fraction(2, 4)

    assert half == two_quarters
    assert half <= two_quarters
    assert half >= two_quarters
    assert not (half < two_quarters)
    assert not (half > two_quarters)
    assert not (half != two_quarters)


def test_ordering() -> None:
    """Order fractions with different signs and denominators."""
    third = Fraction(1, 3)
    half = Fraction(1, 2)

    assert third != half
    assert third < half
    assert third <= half
    assert half > third
    assert half >= third
    assert Fraction(-1, 2) < Fraction(-1, 3)


def test_addition() -> None:
    """Add fractions with different denominators."""
    assert Fraction(1, 2) + Fraction(1, 3) == Fraction(5, 6)


def test_multiplication() -> None:
    """Multiply fractions and simplify result."""
    assert Fraction(-2, 3) * Fraction(3, 4) == Fraction(-1, 2)


def test_string_formatting() -> None:
    """Check the readable and developer representations."""
    fraction = Fraction(6, 8)

    assert str(fraction) == "3/4"
    assert repr(fraction) == "Fraction(3, 4"
