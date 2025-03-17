import heapq
import sqlite3

from collections import defaultdict

import numpy as np

import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

from .utils import DB_FILE, holiday_dates, full_dates, missing_dates, partial_dates, YEARS

SIZE = 100

def create_histogram(data: list[tuple[int, float, float]]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Creates a histogram of traffic density from data

    Args:
        data: list[tuple[float, float, int]]: List of tuples of volume, latitude, longitude
        
    Returns:
        tuple[np.ndarray, np.ndarray, np.ndarray]: Tuple containing density heatmap, x_edges, y_edges, where x_edges is latitudes and y_edges in longitudes
    """
    
    vols = []
    lats = []
    longs = []
    for vol, lat, long in data:
        vols.append(vol)
        lats.append(lat)
        longs.append(long)
    
    # Creates bins for latitudes and longitudes
    num_bins = SIZE
    lat_bins = np.linspace(min(lats), max(lats), num_bins)
    long_bins = np.linspace(min(longs), max(longs), num_bins)

    # Creates a 2D histogram of traffic density
    density_matrix, x_edges, y_edges = np.histogram2d(lats, longs, bins=[lat_bins, long_bins], weights=vols)

    # Applied a Gaussian filter to the density matrix
    sigma = 1.2  # Standard deviation (changes the radius width)
    density_heatmap = gaussian_filter(density_matrix, sigma=sigma)

    return density_heatmap, x_edges, y_edges
    
def index_of_closest(arr: list, val: float) -> int:
    """Returns index of closest value in list/array

    Args:
        arr (list): Array of values
        val (float): Value to find closest to

    Returns:
        int: Index of closest value in array
    """
    return min(((abs(val*1000 - j*1000), i) for i, j in enumerate(arr)), key=lambda x:x[0])[1]

def euclidean_distance(point1: tuple[int, int], point2: tuple[int, int]) -> float:
    """Gets euclidean distance between 2 points

    Args:
        point1 (tuple[int, int]): Point 1
        point2 (tuple[int, int]): Point 2

    Returns:
        float: Distance
    """
    
    return np.sqrt(
        (point1[0] - point2[0])**2 
        + (point1[1] - point2[1])**2
    )
    
def pathfind(hist: np.ndarray, x_edges: np.ndarray, y_edges: np.ndarray, start: tuple[float, float], dest: tuple[float, float]) -> list[tuple[int, int]]: 
    """Implementation of the A* pathfinding algorithm

    Args:
        hist (np.ndarray): Traffic density heatmap
        x_edges (np.ndarray): Latitudes
        y_edges (np.ndarray): Longitudes
        start (tuple[float, float]): Start point
        dest (tuple[float, float]): Destination point

    Returns:
        list[tuple[int, int]]: List of points in path
    """
    # Snaps to closest bins
    start_long = index_of_closest(y_edges, start[0])
    start_lat = index_of_closest(x_edges, start[1])
    
    # Ensures start point is within bounds
    if start_long >= SIZE:
        start_long = SIZE - 1
    if start_lat >= SIZE:
        start_lat = SIZE - 1

    # Snaps to closest bins
    dest_long = index_of_closest(y_edges, dest[0])
    dest_lat = index_of_closest(x_edges, dest[1])
    
    # Ensures destination point is within bounds
    if dest_long >= SIZE:
        dest_long = SIZE - 1
    if dest_lat >= SIZE:
        dest_lat = SIZE - 1
    
    start_transposed = (start_long, start_lat)
    dest_transposed = (dest_long, dest_lat)
    
    # Below is the A* algorithm
    came_from = {}
    
    g_score = defaultdict(lambda: float("inf"))
    g_score[start_transposed] = 0
    
    f_score = defaultdict(lambda: float("inf"))
    f_score[start_transposed] = euclidean_distance(start_transposed, dest_transposed)
    
    open_set = [(f_score[start_transposed], start_transposed)]
    
    while open_set:
        current_f, current = heapq.heappop(open_set)
        
        if current == dest_transposed:
            total_path = [current]
            while current in came_from.keys():
                current = came_from[current]
                total_path.append(current)
            total_path.reverse()
            return total_path
        
        neighbours = []
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            neighbour = (current[0] + dx, current[1] + dy)
            if 0 <= neighbour[0] < SIZE and 0 <= neighbour[1] < SIZE:
                neighbours.append(neighbour)
        
        for neighbour in neighbours:
            tentative_g_score = g_score[current] + hist[neighbour[0]][neighbour[1]] / 1000
            if tentative_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = tentative_g_score
                f_score[neighbour] = g_score[neighbour] + euclidean_distance(neighbour, dest_transposed)
                if neighbour not in open_set:
                    heapq.heappush(open_set, (f_score[neighbour], neighbour))
    
    return []
    
if __name__ == "__main__":
    for year in YEARS:
        if year == 2024:
            for date in partial_dates:
                hist, x_edges, y_edges = create_histogram(date, year)
                # print(x_edges, y_edges)
                # print(hist.shape)
                # print(hist[98])
                
                path = pathfind(hist, x_edges, y_edges, (-6.33, 53.32), (-6.21, 53.37))
                # print(path)
                plt.imshow(hist, origin="lower", cmap="hot", aspect="auto")
                plt.colorbar(label="Traffic Density")
                plt.title(f"{date} {year}")
                plt.xlabel("Longitude")
                plt.ylabel("Latitude")
                ax = plt.gca()
                ax.set_aspect('equal', adjustable='box')
                
                path_x = [p[1] for p in path]  # Extract x-coordinates (longitude)
                path_y = [p[0] for p in path]  # Extract y-coordinates (latitude)
                plt.plot(path_x, path_y, 'b-', label='Path')  # Plot the path with blue circles and lines
                # print(path)
                plt.show()
        else:
            for date in full_dates:
                hist, x_edges, y_edges = create_histogram(date, year)
                # print(x_edges, y_edges)
                # print(hist.shape)
                # print(hist[98])
                
                path = pathfind(hist, x_edges, y_edges, (-6.33, 53.32), (-6.21, 53.37))
                # print(path)
                plt.imshow(hist, origin="lower", cmap="hot", aspect="auto")
                plt.colorbar(label="Traffic Density")
                plt.title(f"{date} {year}")
                plt.xlabel("Longitude")
                plt.ylabel("Latitude")
                ax = plt.gca()
                ax.set_aspect('equal', adjustable='box')
                
                path_x = [p[1] for p in path]  # Extract x-coordinates (longitude)
                path_y = [p[0] for p in path]  # Extract y-coordinates (latitude)
                plt.plot(path_x, path_y, 'b-', label='Path')  # Plot the path with blue circles and lines
                # print(path)
                plt.show()