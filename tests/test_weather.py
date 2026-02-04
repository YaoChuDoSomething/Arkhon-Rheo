import datetime

import pytest

from src.weather_processor import PREFIX, SUFFIX, format_weather_filename


def test_format_weather_filename_basic():
    """Test basic filename formatting with a known datetime."""
    dt = datetime.datetime(2020, 5, 20, 0, 0)
    expected = f"{PREFIX}_20200520_0000{SUFFIX}"
    assert format_weather_filename(dt) == expected


def test_format_weather_filename_midnight():
    """Test filename formatting at midnight."""
    dt = datetime.datetime(2024, 1, 1, 0, 0)
    expected = f"{PREFIX}_20240101_0000{SUFFIX}"
    assert format_weather_filename(dt) == expected


def test_format_weather_filename_end_of_day():
    """Test filename formatting at the very end of a day."""
    dt = datetime.datetime(2023, 12, 31, 23, 59)
    expected = f"{PREFIX}_20231231_2359{SUFFIX}"
    assert format_weather_filename(dt) == expected


@pytest.mark.parametrize(
    ("year", "month", "day", "hour", "minute", "expected_ts"),
    [
        (2021, 6, 15, 12, 30, "20210615_1230"),
        (1999, 12, 31, 23, 59, "19991231_2359"),
        (2000, 1, 1, 0, 0, "20000101_0000"),
    ],
)
def test_format_weather_filename_parameterized(
    year, month, day, hour, minute, expected_ts
):
    """Test multiple datetime scenarios using parametrization."""
    dt = datetime.datetime(year, month, day, hour, minute)
    expected = f"{PREFIX}_{expected_ts}{SUFFIX}"
    assert format_weather_filename(dt) == expected
