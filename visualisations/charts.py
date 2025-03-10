import sqlite3
from pathlib import Path

import geopandas
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px


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

missing_dates = [
    "Easter Monday",
    "October Bank Holiday",
    "Christmas Day",
    "St Stephen's Day"
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


def generate_heatmap(holiday: str, year: int, show_points: bool=False):
    """Generates heatmap plot
    
    Args:
        holiday (str): Holiday to search for
        year (int): Year to search for
        show_points (bool): Shows points if true
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

    xi = np.linspace(min(longs), max(longs), 100)
    yi = np.linspace(min(lats), max(lats), 100)
    zi = griddata((longs, lats), vols, (xi[None,:], yi[:,None]), method='cubic')
    
    # CS = plt.contour(xi,yi,zi,25,linewidths=0.2,colors='k', vmin=0)
    plt.pcolor(xi, yi, zi, cmap=plt.cm.Reds, vmin=0)
    
    CS = plt.contourf(xi,yi,zi,20,cmap=plt.cm.Reds, vmin = 0)

    plt.colorbar()
    if show_points:
        plt.scatter(longs, lats, marker='o', c='b', s=0.1)
    plt.title(f"Congestion Colourbar For {holiday} {year}")
    plt.axis([min(longs) - 0.01, max(longs) + 0.01, min(lats) - 0.01, max(lats) + 0.01])
    plt.savefig("figure")

def generate_barchart(holiday: str):
    """Generates barchart plot
    
    Args:
        holiday (str): Holiday to search for
    """
    dates = []
    for year in YEARS:
        if holiday in missing_dates and year == 2024:
            continue
        dates.append(holiday_dates[year][holiday])
        
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    
    data = []
    for date in dates:
        if holiday in missing_dates and date[0] == 2024:
            continue
        cur.execute("SELECT SUM(sum_volume) FROM data WHERE year=? AND month=? AND day=?", (date[0], date[1], date[2]))
        data.append(cur.fetchall()[0][0])
    
    if holiday in missing_dates:
    
        fig = px.bar(
            {
                "Year": YEARS[:-1], 
                "Total Vehicles Passing Sites": data
            }, 
            x="Year", 
            y="Total Vehicles Passing Sites",
            title=f"Total Congestion On {holiday}"
        ).update_layout(
            xaxis = dict(
                dtick = 1
            )
        )
    else:
        fig = px.bar(
            {
                "Year": YEARS, 
                "Total Vehicles Passing Sites": data
            },
            x="Year", 
            y="Total Vehicles Passing Sites",
            title=f"Total Congestion On {holiday}"
        ).update_layout(
            xaxis = dict(
                dtick = 1
            )
        )
    
    path = BASE / f"charts/bar/{holiday}.html"
    file = open(path, "a+")
    file.close()
    fig.write_html(path)
    
if __name__ == "__main__":
    # generate_heatmap(full_dates[0], YEARS[0])
    for date in full_dates:
        generate_barchart(date)
    # generate_heatmap(full_dates[0], YEARS[0], True)
        # for i in range(len(full_dates)):
        #     generate_heatmap(full_dates[i], YEARS[0])