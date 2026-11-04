"""Tests for the weather functions."""

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from weather_kl3901 import (
    celsius_to_fahrenheit,
    clean_readings,
    summarize_temperatures,
)


@pytest.mark.parametrize("celsius, expected", [
    (0, 32),
    (100, 212),
    (-40, -40),
    (37, 98.6),
    (-273.15, -459.67),
])
def test_celsius_to_fahrenheit(celsius, expected):
    """Check temperature conversions."""
    result = celsius_to_fahrenheit(celsius)
    assert result == pytest.approx(expected)


@pytest.mark.parametrize("bad_input, expected_error", [
    ("cold", TypeError),
    (None, TypeError),
    ([], TypeError),
    (-273.16, ValueError),
])
def test_celsius_to_fahrenheit_invalid(bad_input, expected_error):
    """Check that invalid inputs raise the expected errors."""
    with pytest.raises(expected_error):
        celsius_to_fahrenheit(bad_input)


def test_summarize_temperatures():
    """Check the summary when one temperature is missing."""
    # Arrange
    temps = [10.0, float("nan"), 20.0]

    # Act
    result = summarize_temperatures(temps)

    # Assert
    assert result["mean"] == pytest.approx(15.0)
    assert result["min"] == pytest.approx(10.0)
    assert result["max"] == pytest.approx(20.0)
    assert result["n_missing"] == 1


@pytest.fixture
def raw_readings():
    """Return raw station readings for the tests."""
    return pd.DataFrame({
        "station": ["JFK", "CPK", "JFK", "CPK", "LGA"],
        "date": [
            "2026-07-02",
            "2026-07-01",
            "2026-07-01",
            "2026-07-02",
            "2026-07-01",
        ],
        "temp_c": [30.0, 25.0, float("nan"), 999.0, 28.0],
    })


def test_raw_readings_fixture(raw_readings):
    """Check the columns, row count, and missing values."""
    assert raw_readings.columns.tolist() == ["station", "date", "temp_c"]
    assert raw_readings.shape[0] == 5
    assert raw_readings.isna().sum().sum() == 1


def test_clean_readings(raw_readings):
    """Check the cleaned readings against the expected DataFrame."""
    expected = pd.DataFrame({
        "station": ["CPK", "JFK", "LGA"],
        "date": ["2026-07-01", "2026-07-02", "2026-07-01"],
        "temp_c": [25.0, 30.0, 28.0],
        "temp_f": [77.0, 86.0, 82.4],
    })

    result = clean_readings(raw_readings)

    assert_frame_equal(result, expected)