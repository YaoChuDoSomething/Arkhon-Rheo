import datetime
from typing import Final

# Naming convention: era5_20200520_0000.nc
PREFIX: Final[str] = "era5"
SUFFIX: Final[str] = ".nc"


def format_weather_filename(dt: datetime.datetime) -> str:
    """
    Constructs filename based on the prefix_tsfmt.nc convention.

    Args:
        dt: The datetime object to format.

    Returns:
        A string representing the formatted filename.
    """
    timestamp_str: str = dt.strftime("%Y%m%d_%H%M")
    return f"{PREFIX}_{timestamp_str}{SUFFIX}"


def main() -> None:
    target_date = datetime.datetime(2020, 5, 20, 0, 0)
    era5_filename = format_weather_filename(target_date)
    print(f"Targeting: {era5_filename}")


if __name__ == "__main__":
    main()
