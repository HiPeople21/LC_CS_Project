import aiosqlite

import numpy as np
from flask import Flask, render_template, request

from ..visualisations import create_histogram, pathfind
from .utils import BASE, DB_FILE, holiday_dates, RESPONSES_DB, YEARS

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """Home page"""
    return render_template("index.html")

@app.route("/pathfinding", methods=["GET"])
def pathfinding():
    """Pathfinding page"""
    return render_template("pathfinding.html")

@app.route("/get_data", methods=["POST"])
async def get_data():
    """Returns data for heatmap"""
    holiday = request.get_json()["day"]
    start_time = int(request.get_json()["startTime"])
    end_time = int(request.get_json()["endTime"])
    
    con = await aiosqlite.connect(DB_FILE)
    cur = await con.cursor()
    data = {}
    for year in YEARS:
        if year == 2024:
            if holiday_dates[year].get(holiday):
                _, month, day = holiday_dates[year][holiday]
                await cur.execute("SELECT data.site_id, data.sum_volume, sites.latitude, sites.longitude FROM data INNER JOIN sites ON sites.id = data.site_id WHERE month=? AND day=? AND ? <= hour <= ?", (month, day, start_time + 1, end_time));
                for site, vol, lat, long in await cur.fetchall():
                    if site not in data:
                        data[site] = []
                data[site].append((vol, lat, long))
        else:
            _, month, day = holiday_dates[year][holiday]
            await cur.execute("SELECT data.site_id, data.sum_volume, sites.latitude, sites.longitude FROM data INNER JOIN sites ON sites.id = data.site_id WHERE month=? AND day=? AND ? <= hour <= ?", (month, day, start_time + 1, end_time));
            for site, vol, lat, long in await cur.fetchall():
                if site not in data:
                    data[site] = []
                data[site].append((vol, lat, long))
    results = []
    for values in data.values():
        if not values:
            continue
        avg = np.mean([vol for vol, _, _ in values])
        results.append((avg, values[0][1], values[0][2]))
    await cur.close()
    await con.close()
    return results

@app.route("/pathfind", methods=["POST"])
def get_path():
    """Returns pathfinding results"""
    try:
        data = [(point.values()) for point in request.get_json()["data"]]
        start_point = (float(request.get_json()["startLongitude"]), float(request.get_json()["startLatitude"]))
        end_point = (float(request.get_json()["destinationLongitude"]), float(request.get_json()["destinationLatitude"]))

        hist, x_edges, y_edges = create_histogram(data)
        path = pathfind(hist, x_edges, y_edges, start_point, end_point)
        result = [(x_edges[lat], y_edges[long]) for long, lat in path]
        
        return {"status": "success", "path":result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route("/statistics", methods=["GET"])
def statistics():
    """Statistics page"""
    return render_template("statistics.html")

@app.route("/responses", methods=["GET"])
async def responses():
    """Responses page"""
    con = await aiosqlite.connect(RESPONSES_DB)
    cur = await con.cursor()
    await cur.execute("SELECT * FROM responses")
    responses = await cur.fetchall()
    await con.commit()
    await con.close()
    return render_template("responses.html", responses=responses)

@app.route("/feedback", methods=["POST"])
async def feedback():
    """Submits feedback"""
    try:
        holiday = request.get_json()["day"]
        start_time = int(request.get_json()["startTime"])
        end_time = int(request.get_json()["endTime"])
        start_location = (request.get_json()["startLatitude"], request.get_json()["startLongitude"])
        end_location = (request.get_json()["destinationLatitude"], request.get_json()["destinationLongitude"])
        submit_time = request.get_json()["submitTime"]
        helpful = request.get_json()["helpful"]
        con = await aiosqlite.connect(RESPONSES_DB)
        cur = await con.cursor()
        
        await cur.execute("INSERT INTO responses (submission_time, holiday, time_range, start_location, destination, helpful) VALUES (?, ?, ?, ?, ?, ?)", (submit_time, holiday, f"{start_time}:00-{end_time}:00", str(start_location), str(end_location), helpful))
        await con.commit()
        return {"status": "success", "message": ""}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        await cur.close()
        await con.close()

if __name__ == "__main__":
    app.run(debug=True)