# Utility functions
import calendar
import csv
import datetime as dt

from datetime import datetime, timedelta
from pathlib import Path
BASE = Path(__file__).parent

YEARS = [2020, 2021, 2022, 2023, 2024]

MONTHS = [
    "",  # This element left blank as January will be at index 1
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

MISSING_DATA = [
    BASE / "data/2024/SCATSApril2024.csv",
    BASE / "data/2024/SCATSDecember2024.csv"
]


def generate_holiday_dates(year: int) -> list[dt.datetime]:
    """Returns the holiday dates for a given year.
    
    Args:
        year (int): The year to generate dates for
        
    Returns:
        list[dt.datetime]: A list of datetime.datetime objects
    """
    
    # Dates same every year
    new_years = datetime(year, 1, 1)
    st_patricks = datetime(year, 3, 17)
    christmas = datetime(year, 12, 25)
    st_stephens = datetime(year, 12, 26)
    
    # Bank holidays
    may_bank_holiday = get_first_nday_of_month(0, 5, year)
    june_bank_holiday = get_first_nday_of_month(0, 6, year)
    august_bank_holiday = get_first_nday_of_month(0, 8, year)
    october_bank_holiday = get_last_nday_of_month(0, 10, year)
    
    # St Brigid's Day and Easter Monday require more complex computation
    st_brigids = datetime(year, 2, 1)
    if st_brigids.weekday() != 4:  # If it's not a Friday
        st_brigids = get_first_nday_of_month(0, 2, year)
        
    easter_monday = gregorian_easter_monday(year)
    
    return [
        new_years,
        st_brigids,
        st_patricks,
        easter_monday,
        may_bank_holiday,
        june_bank_holiday,
        august_bank_holiday,
        october_bank_holiday,
        christmas,
        st_stephens
    ]
    
        
def get_first_nday_of_month(weekday: int, month: int, year: int) -> int:
    """Returns the first instance of a weekday in a given month
    
    Args:
        weekday (int): The weekday to generate for, where Monday is 0, Tuesday is 1 etc
        month (int): The month of the given day
        year (int): The year of the given day
        
    Returns:
        dt.datetime: The date of the given day
    """

    reference_day = datetime(year, month, 7)
    offset = -((reference_day.weekday() - weekday) % 7)
    return reference_day + timedelta(offset)


def get_last_nday_of_month(weekday: int, month: int, year: int) -> int:
    """Returns the last instance of a weekday in a given month
    
    Args:
        weekday (int): The weekday to generate for, where Monday is 0, Tuesday is 1 etc
        month (int): The month of the given day
        year (int): The year of the given day
        
    Returns:
        dt.datetime: The date of the given day
    """

    reference_day = datetime(year, month, calendar.monthrange(year, month)[1])
    offset = -((reference_day.weekday() - weekday) % 7)
    return reference_day + timedelta(offset)


def gregorian_easter_monday(year: int) -> dt.date:
    """Returns date of Easter Monday for a given year
    Algorithm found here: https://en.wikipedia.org/wiki/Date_of_Easter#Anonymous_Gregorian_algorithm
    
    Args:
        year (int): Year of Easter Monday

    Returns:
        dt.date: Date of Easter Monday
    """
    
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    g = (8*b + 13) // 25
    h = (19*a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2*e + 2*i - h - k) % 7
    m = (a + 11*h + 19*i) // 433
    n = (h + l - 7*m + 90) // 25
    p = (h + l - 7*m + 33*n + 19) % 32
    # Adds one as algorithm finds Easter Sunday, when Easter Monday is the date required
    return datetime(year, n, p) + timedelta(1)


def parse_date(date_: str, year_: int) -> list[int]:
    """Parses the date string as a tuple of integers
    
    Date formats
    - 2020: 
        - First half: '2020-06-01 00:00:00.000' 
        - Second half: '20200801000000'
    - 2021: '20210101000000'
    - 2022: '20220131120000'
    - 2023: '20230131060000'
    - 2024: '20240130230000'
    
    Args:
        date (str): The date string
        year (int): The year of the date

    Returns:
        list[int]: The year, month, day, hour, minute, second
    """

    if year_ == 2020:
        try:
            date, time = date_.split(" ")
            year, month, day = date.split("-")
            hour, minute, second = time.split(":")
            
            year = int(year)
            month = int(month)
            day = int(day)
            
            hour = int(hour)
            minute = int(minute)
            second = float(second)
        except ValueError:  # Second half of year
            year = int(date_[:4])
            month = int(date_[4:6])
            day = int(date_[6:8])
            hour = int(date_[8:10])
            minute = int(date_[10:12])
            second = float(date_[12:])
    elif year_ in (2021, 2022, 2023, 2024):
        year = int(date_[:4])
        month = int(date_[4:6])
        day = int(date_[6:8])
        hour = int(date_[8:10])
        minute = int(date_[10:12])
        second = float(date_[12:])
    return [year, month, day, hour, minute, second]


def get_site_data() -> None:
    """Returns the site data

    Returns:
        list[dict]: The site data. Keys are 'SiteID', 'Site_Description_Cap', 'Site_Description_Lower', 'Region', 'Lat', 'Long', 'Site_Type'
    """
    path = BASE / "dcc_traffic_signals_20221130.csv"

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)
    
if __name__ == "__main__":
    print(get_last_nday_of_month(0, 5, 2024))