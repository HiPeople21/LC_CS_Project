import sqlite3
from pathlib import Path

import geopandas
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

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

    fig = px.density_map(
        {
            "Latitude": lats,
            "Longitude": longs,
            "Volume": vols                  
        }, 
        lat='Latitude', 
        lon='Longitude', 
        z='Volume', radius=10,
        center=dict(lat=53.345481, lon=-6.275819), 
        zoom=10.5,
        map_style="open-street-map",
        
    )
    fig.update_layout(
        dragmode=False
    )

    path = BASE / f"charts/heatmap/{holiday}-{year}.html"
    file = open(path, "a+")
    file.close()
    fig.write_html(path, config={"scrollZoom": False}, full_html=False)
    
    
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
    
    # Creates file
    file = open(path, "a+")
    file.close()
    
    fig.write_html(path, full_html=False)
    
if __name__ == "__main__":
    # for year in YEARS:
    #     if year == 2024:
    #         for date in partial_dates:
    #             generate_heatmap(date, year)
    #     else:
    #         for date in full_dates:
    #             generate_heatmap(date, year)
    for date in full_dates:
        generate_barchart(date)