import csv
from flask import Flask, render_template, jsonify, request
from pyproj import Transformer

app = Flask(__name__)

# British National Grid -> WGS84. always_xy=True means (x, y) in -> (lon, lat) out.
transformer = Transformer.from_crs("EPSG:27700", "EPSG:4326", always_xy=True)

def load_sites(path="data/FW_Fish_Sites_2026-09-20.csv"):
    sites = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                easting = float(row["SITE_RANKED_EASTING"])
                northing = float(row["SITE_RANKED_NORTHING"])
            except (ValueError, KeyError):
                continue  # skip rows with missing coordinates
            lon, lat = transformer.transform(easting, northing)
            sites.append({
                "id": int(row["SITE_ID"]),
                "name": row["SITE_NAME"],
                "waterbody": row["SITE_PARENT_NAME"],
                "surveys": row["N_SURVEYS"],
                "lat": lat,
                "lon": lon,
            })
    return sites

SITES = load_sites()  # loaded once at startup

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/info")
def info():
    return render_template("info.html")

@app.route("/data")
def data():
    return render_template("data.html")

@app.route("/map")
def map_page():          # renamed so it doesn't shadow Python's built-in map()
    return render_template("map.html")

@app.route("/api/sites")
def api_sites():
    return jsonify(SITES)

@app.route("/dashboard")
def dashboard():
    site_id = request.args.get("site_id", type=int)
    site = next((s for s in SITES if s["id"] == site_id), None)
    return render_template("dashboard.html", site=site)

if __name__ == "__main__":
    app.run(debug=True)