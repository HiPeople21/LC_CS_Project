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
    a = most_traffic()
    print(f"Site {a[12]} had the most traffic at {a[4]}/{a[5]}/{a[6]} {a[7]}:{a[8]}:{a[9]} with an average of {a[17]} vehicles")
    
    b = most_year()
    print(f"{b[0]} had the most traffic average at {b[1]}")
    
    c = most_holiday()
    print(f"{c[0]} had the most traffic average at {c[1]}")
    
    d = most_time()
    print(f"{int(d[0]) - 1}:00 - {int(d[0])}:00 had the most traffic average at {d[1]}")
    
    e = most_site_overall()
    print(f"{e[0]["Site_Description_Cap"]} had the most traffic average at {e[1][1]}")
    
    f = least_year()
    print(f"{f[0]} had the least traffic average at {f[1]}")
    
    g = least_holiday()
    print(f"{g[0]} had the least traffic average at {g[1]}")
    
    h = least_time()
    print(f"{int(h[0]) - 1}:00 - {int(h[0])}:00 had the least traffic average at {h[1]}")
    
    i = least_site_overall()
    print(f"{i[0]["Site_Description_Cap"]} had the least traffic average at {i[1][1]}")