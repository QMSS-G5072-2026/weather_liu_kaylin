# read version from installed package
from importlib.metadata import version

from .weather_kl3901 import (
    celsius_to_fahrenheit,
    clean_readings,
    summarize_temperatures,
)

__version__ = version("weather_kl3901")