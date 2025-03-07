import sqlite3
from pathlib import Path

import geopandas
import matplotlib.pyplot as plt
import numpy as np

from scipy.interpolate import griddata

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

holiday_dates = {}
for year in YEARS:
    dates = generate_holiday_dates(year)
    holiday_dates[year] = {}
    if year != 2024:
        for i, date in enumerate(full_dates):
            holiday_dates[year][date] = (dates[i].year, dates[i].month, dates[i].day)
    elif year == 2024:
        for i, date in enumerate(partial_dates):
            holiday_dates[year][date] = (dates[i].year, dates[i].month, dates[i].day)


def generate_heatmap(holiday: str, year: int):
    """Generates heatmap plot
    
    Args:
        holiday (str): Holiday to search for
        year (int): Year to search for
    """
    date = holiday_dates[year][holiday]
    fig, ax = plt.subplots()
    shapefile = geopandas.read_file(BASE / "dublin_boundary_epsg_4326/dublin_boundary_epsg_4326/dublin_boundary_epsg_4326.shp")
    shapefile.boundary.plot(ax=ax)
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute("SELECT data.sum_volume, sites.latitude, sites.longitude FROM data INNER JOIN sites ON sites.id = data.site_id WHERE year=? AND month=? AND day=? ", (date[0], date[1], date[2]))

    vols = []
    lats = []
    longs = []
    for vol, lat, long in cur.fetchall():
        vols.append(vol)
        lats.append(lat)
        longs.append(long)
    
    xi = np.linspace(min(longs), max(longs),100)
    yi = np.linspace(min(lats), max(lats),100)
    zi = griddata((longs, lats), vols, (xi[None,:], yi[:,None]), method='cubic')

    CS = plt.contourf(xi,yi,zi,25,cmap=plt.cm.Reds)
    cbar = plt.colorbar()
    cbar.ax.set_ylim(0)

    # plt.scatter(longs,lats,marker='o',c='b',s=0.5)

    plt.title(f"Congestion Colourbar For {holiday} {year}")
    plt.xlim(min(longs) - 0.02, max(longs) + 0.02)
    plt.ylim(min(lats) - 0.02, max(lats) + 0.02)
    plt.show()

def generate_barchart(holiday: str):
    """Generates barchart plot
    
    Args:
        holiday (str): Holiday to search for
    """
    dates = []
    for year in YEARS:
        dates.append(holiday_dates[year][holiday])
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    data = []
    for date in dates:
        cur.execute("SELECT SUM(sum_volume) FROM data WHERE year=? AND month=? AND day=?", (date[0], date[1], date[2]))
        data.append(cur.fetchall()[0][0])
    fig, ax = plt.subplots()
    plt.title(f"Total Congestion On {holiday}")
    ax.bar(YEARS, data)
    ax.ticklabel_format(style='plain')  # Prevents number from being converted to scientific notation
    plt.xlabel("Year")
    plt.ylabel("Total Vehicles Passing Sites")
    plt.show()
if __name__ == "__main__":
    generate_heatmap(full_dates[0], YEARS[0])