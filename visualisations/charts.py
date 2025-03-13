import sqlite3

import plotly.express as px

from .utils import BASE, DB_FILE, holiday_dates, full_dates, missing_dates, partial_dates, YEARS

def generate_heatmap(holiday: str, year: int):
    """Generates heatmap plot
    
    Args:
        holiday (str): Holiday to search for
        year (int): Year to search for
    """
    date = holiday_dates[year][holiday]
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
    

    # Creates file
    path = BASE / f"charts/heatmap/{holiday}-{year}.html"
    file = open(path, "a+")
    file.close()
    
    # Saves figure and prevents zooming as the point radii don't scale with zoom
    fig.update_layout(
        dragmode=False
    )
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
                "Year": YEARS[:-1],  # Excludes 2024 data (does not exist)
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