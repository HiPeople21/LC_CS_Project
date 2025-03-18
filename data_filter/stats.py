import sqlite3

import numpy as np

from .utils import BASE, get_site_data, YEARS
from ..visualisations.utils import full_dates, holiday_dates, missing_dates

def most_traffic():
    """
    Returns the site with the most traffic
    """
    con = sqlite3.connect(BASE / "database.db")
    cur = con.cursor()
    cur.execute("SELECT *, AVG(data.sum_volume) FROM data INNER JOIN SITES ON data.site_id = sites.id")
    most_once = cur.fetchall()[0]
    con.close()
    return most_once
    
def most_year():
    """
    Returns the site with the most traffic on a year
    """
    con = sqlite3.connect(BASE / "database.db")
    cur = con.cursor()
    cur.execute("SELECT year, AVG(sum_volume) FROM data GROUP BY year")
    most_ = cur.fetchall()
    con.close()
    return sorted(most_, key=lambda x: x[1])[-1]
  
def most_holiday():
    """
    Returns the site with the most traffic on a holiday
    """
    con = sqlite3.connect(BASE / "database.db")
    cur = con.cursor()
    res = {}
    final = {}
    for holiday in full_dates:
        res[holiday] = []
        for year in YEARS:
            if year == 2024 and holiday in missing_dates:
                continue
            cur.execute("SELECT AVG(sum_volume) FROM data WHERE month=? AND day=? AND year=?", (holiday_dates[year][holiday][1], holiday_dates[year][holiday][2], year))
            res[holiday].append(cur.fetchall()[0][0])
        final[holiday] = np.mean(res[holiday])
    con.close()
    return max(final.items(), key=lambda x: x[1])

def most_time():
    """
    Returns the site with the most traffic at a certain time
    """
    con = sqlite3.connect(BASE / "database.db")
    cur = con.cursor()
    cur.execute("SELECT hour, AVG(sum_volume) FROM data GROUP BY hour")
    most_ = cur.fetchall()       
    con.close()
    return max(most_, key=lambda x: x[1])

def most_site_overall():
    """
    Returns the site with the most traffic overall
    """
    con = sqlite3.connect(BASE / "database.db")
    cur = con.cursor()
    cur.execute("SELECT site_id, AVG(sum_volume) FROM data GROUP BY site_id")
    most_ = cur.fetchall()
    most_ = max(most_, key=lambda x: x[1])
    con.close()
    site_data = get_site_data()
    for site in site_data:
        if int(site["SiteID"]) == most_[0]:
            return site, most_

def least_year():
    """
    Returns the site with the least traffic on a year
    """
    con = sqlite3.connect(BASE / "database.db")
    cur = con.cursor()
    cur.execute("SELECT year, AVG(sum_volume) FROM data GROUP BY year")
    least_ = cur.fetchall()
    con.close()
    return sorted(least_, key=lambda x: x[1])[0]
  
def least_holiday():
    """
    Returns the site with the least traffic on a holiday
    """
    con = sqlite3.connect(BASE / "database.db")
    cur = con.cursor()
    res = {}
    final = {}
    for holiday in full_dates:
        res[holiday] = []
        for year in YEARS:
            if year == 2024 and holiday in missing_dates:
                continue
            cur.execute("SELECT AVG(sum_volume) FROM data WHERE month=? AND day=? AND year=?", (holiday_dates[year][holiday][1], holiday_dates[year][holiday][2], year))
            res[holiday].append(cur.fetchall()[0][0])
        final[holiday] = np.mean(res[holiday])
    con.close()
    return min(final.items(), key=lambda x: x[1])

def least_time():
    """
    Returns the site with the least traffic at a certain time
    """
    con = sqlite3.connect(BASE / "database.db")
    cur = con.cursor()
    cur.execute("SELECT hour, AVG(sum_volume) FROM data GROUP BY hour")
    least_ = cur.fetchall()       
    con.close()
    return min(least_, key=lambda x: x[1])

def least_site_overall():
    """
    Returns the site with the least traffic overall
    """
    con = sqlite3.connect(BASE / "database.db")
    cur = con.cursor()
    cur.execute("SELECT site_id, AVG(sum_volume) FROM data GROUP BY site_id")
    least_ = cur.fetchall()
    least_ = min(least_, key=lambda x: x[1])
    con.close()
    site_data = get_site_data()
    for site in site_data:
        if int(site["SiteID"]) == least_[0]:
            return site, least_
    return

if __name__ == "__main__":
    print(most_traffic())
    print(most_year())
    print(most_holiday())
    print(most_time())
    print(most_site_overall())
    
    print(least_year())
    print(least_holiday())
    print(least_time())
    print(least_site_overall())
    