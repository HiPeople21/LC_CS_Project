import sqlite3
from pathlib import Path

from ..data_filter.utils import generate_holiday_dates, YEARS

BASE = Path(__file__).parent
DB_FILE = BASE.parent / "data_filter/database.db"
RESPONSES_DB = BASE / "responses.db"

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
            
def create_db(file: str|Path):
    """Creates the responses database"""
    con = sqlite3.connect(file)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS responses (id INTEGER PRIMARY KEY, submission_time TEXT, holiday TEXT, start_time INTEGER, end_time INTEGER, start_latitude REAL, start_longitude REAL, destination_latitude REAL, destination_longitude REAL, helpful BOOL)")
    con.commit()
    con.close()

if __name__ == "__main__":
    # print(holiday_dates)
    create_db(RESPONSES_DB)
    # con = sqlite3.connect(RESPONSES_DB)
    # cur = con.cursor()
    # cur.execute("SELECT sql FROM sqlite_schema;")
    # print(cur.fetchall())
    # con.commit()
    # con.close()