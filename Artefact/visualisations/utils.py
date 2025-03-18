from pathlib import Path

from ..data_filter.utils import generate_holiday_dates, YEARS

BASE = Path(__file__).parent
DB_FILE = BASE.parent / "data_filter/database.db"


full_dates = [
    "New Year's Day",
    "St Brigid's Day",
    "St Patrick's Day",
    "Easter Monday",
    "May Bank Holiday",
    "June Bank Holiday",
    "August Bank Holiday",
    "October Bank Holiday",
    "Christmas Day",
    "St Stephen's Day"
]

partial_dates = [
    "New Year's Day",
    "St Brigid's Day",
    "St Patrick's Day",
    "May Bank Holiday",
    "June Bank Holiday",
    "August Bank Holiday"
]

missing_dates = [
    "Easter Monday",
    "October Bank Holiday",
    "Christmas Day",
    "St Stephen's Day"
]


# Creates dates for each year
holiday_dates = {}
for year in YEARS:
    dates = generate_holiday_dates(year)
    holiday_dates[year] = {}
    if year != 2024:
        for i, date in enumerate(full_dates):
            holiday_dates[year][date] = (dates[i].year, dates[i].month, dates[i].day)
    elif year == 2024:
        dates = dates[0:3] + dates[4:7]
        for i, date in enumerate(partial_dates):
            holiday_dates[year][date] = (dates[i].year, dates[i].month, dates[i].day)