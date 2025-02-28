# Compiles the data further
import csv
import sqlite3

from pathlib import Path

from utils import BASE, generate_holiday_dates, get_site_data, MISSING_DATA, MONTHS, YEARS

DB_FILE = BASE / "database.db"

def secondary_filter() -> None:
    """
    Reads CSV files and compiles data together by site instead of having separate data for each detector
    """
    site_data = get_site_data()
    data = {}
    site_ids = [site["SiteID"] for site in site_data]
    site_ids_needed = set()
    for year in YEARS:
        dates = generate_holiday_dates(year)
        months = {date.month for date in dates}
        files = [f"SCATS{MONTHS[month]}{year}.csv" for month in months]
        for file in files:
            path = BASE / f"output_data/{year}" / file
            if path in [
                BASE / "output_data/2024/SCATSApril2024.csv",
                BASE / "output_data/2024/SCATSDecember2024.csv"
            ]:
                continue
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["Site"] in site_ids:
                        site_ids_needed.add(row["Site"])
                        data_key = (row["Site"], row["Year"], row["Month"], row["Day"], row["Hour"])
                        if data.get(data_key):
                            data[data_key]["Sum_Volume"] += int(row["Sum_Volume"])
                            data[data_key]["Avg_Volume"] += "," + row["Avg_Volume"]
                        else:
                            data[data_key] = row.copy()
                            data[data_key]["Sum_Volume"] = int(row["Sum_Volume"])
            print(file)
    print(len(data))
    # write_data_to_sql(data, DB_FILE)
    # write_sites_to_sql(site_data, DB_FILE, site_ids_needed)

def display_data_with_sites() -> None:
    """
    Reads CSV files and shows how many rows are usable within each csv file
    """
    site_data = get_site_data()
    site_ids = [site["SiteID"] for site in site_data]
    total = 0
    for year in YEARS:
        dates = generate_holiday_dates(year)
        months = {date.month for date in dates}
        files = [f"SCATS{MONTHS[month]}{year}.csv" for month in months]
        for file in files:
            path = BASE / f"output_data/{year}" / file
            if path in [
                BASE / "output_data/2024/SCATSApril2024.csv",
                BASE / "output_data/2024/SCATSDecember2024.csv"
            ]:
                continue
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                number = 0
                for row in reader:
                    if row["Site"] in site_ids:
                        number += 1
                print(year, file, number)
            total += number
    print(total)


def write_data_to_sql(data: dict[tuple[str, str, str, str, str], dict[str, str | int]], file:str|Path) -> None:
    """Writes data to SQL file
    
    Args:
        data (dict[tuple[str, str, str, str, str], dict[str. str | int]]): Data to be written to file
        file (str): Filename
    """
    con = sqlite3.connect(file)
    cur = con.cursor()
    try:
        for data_item in data.values():
            cur.execute("""
                INSERT INTO data (
                    region,
                    sum_volume,
                    avg_volume,
                    year,
                    month,
                    day,
                    hour,
                    minute,
                    second,
                    site_id
                ) VALUES (?,?,?,?,?,?,?,?,?,?);
            """, (data_item["Region"], data_item["Sum_Volume"], data_item["Avg_Volume"], data_item["Year"], data_item["Month"], data_item["Day"], data_item["Hour"], data_item["Minute"], data_item["Second"], int(data_item["Site"])))
    except Exception as e:
        print(data_item)
        # raise e

    con.commit()
    con.close()

def write_sites_to_sql(sites: list[dict[str, str]], file:str|Path, site_ids_needed: set[str]) -> None:
    """Writes sites to SQL file
    
    Args:
        sites (list[dict[str, str]]): Data to be written to file
        file (str): Filename
        site_ids_needed (set[str]): Site IDs needed
    """
    con = sqlite3.connect(file)
    cur = con.cursor()

    try:
        for site in sites:
            if site["SiteID"] not in site_ids_needed:
                continue
            cur.execute("""
                INSERT INTO sites (
                    id,
                    description,
                    region,
                    latitude,
                    longitude,
                    type
                ) VALUES (?,?,?,?,?,?);
            """, (int(site["SiteID"]), site["Site_Description_Cap"], site["Region"], float(site["Lat"]), float(site["Long"]), site["Site_Type"]))
    except Exception as e:
        print(site)
        raise e


    con.commit()
    con.close()


def create_tables(file:str|Path) -> None:
    """Creates tables
    
    Args:
        file (str): Filename
    """
    con = sqlite3.connect(file)
    cur = con.cursor()

    # Creates sites table
    try:
        cur.execute("""
            CREATE TABLE sites (
                id INTEGER UNIQUE NOT NULL,
                description TEXT,
                region TEXT,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                type TEXT
            );
        """)
    except sqlite3.OperationalError as e:
        print(e)

    # Creates data table
    try:
        cur.execute("""
            CREATE TABLE data (
                id INTEGER UNIQUE NOT NULL,
                region TEXT,
                sum_volume INTEGER NOT NULL,
                avg_volume INTEGER NOT NULL,
                year TEXT NOT NULL,
                month TEXT NOT NULL,
                day TEXT NOT NULL,
                hour TEXT NOT NULL,
                minute TEXT NOT NULL,
                second TEXT NOT NULL,
                site_id INTEGER NOT NULL,
                FOREIGN KEY(site_id) REFERENCES sites(id),
                PRIMARY KEY(id)
            );
        """)
    except sqlite3.OperationalError as e:
        print(e)

    con.commit()
    con.close()

if __name__ == "__main__":
    # create_tables(DB_FILE)
    # secondary_filter()
    # print(get_site_data())
    # create_tables(DB_FILE)
    # con = sqlite3.connect(DB_FILE)
    # cursor = con.cursor()
    # cursor.execute("SELECT * FROM data LIMIT 5;")
    # print(cursor.fetchall())
    # display_data_with_sites()
    pass