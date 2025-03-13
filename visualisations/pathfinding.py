import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter

from .utils import DB_FILE, holiday_dates, full_dates, missing_dates, partial_dates, YEARS


def create_histogram(holiday: str, year:int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Pathfinds

    Args:
        holiday (str): Holiday to find points for
        year (int): Year of holiday
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
    
    
    num_bins = 250
    lat_bins = np.linspace(min(lats), max(lats), num_bins)
    long_bins = np.linspace(min(longs), max(longs), num_bins)

    density_matrix, x_edges, y_edges = np.histogram2d(lats, longs, bins=[lat_bins, long_bins], weights=vols)

    sigma = 2  # Standard deviation
    density_heatmap = gaussian_filter(density_matrix, sigma=sigma)

    plt.imshow(density_heatmap, origin="lower", extent=[min(longs), max(longs), min(lats), max(lats)], cmap="hot", aspect="auto")
    plt.colorbar(label="Traffic Density")
    plt.title("Extracted 2D Density Matrix from `density_mapbox`")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    plt.show()
    
def pathfind(hist: np.ndarray, start: tuple[float, float], dest: tuple[float, float]): 
    pass
    
if __name__ == "__main__":
    #hist, x_edges, y_edges = 
    create_histogram(full_dates[0], YEARS[0])
    
    # print(hist)