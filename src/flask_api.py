from flask import Flask, request, jsonify
import sqlite3 as db
import logging
import sys

from src.xconfig import DefaultConfig as config

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger("api_endpoint")

app = Flask(__name__)


def get_db_cursor():
    db_con = db.connect(config.DATABASE_PATH)
    db_con.row_factory = db.Row
    return db_con.cursor()


@app.route('/')
def hello():
    return 'Welcome to API page'


@app.route('/api/weather')
def get_weather():
    wx_data = []
    try:
        page = request.args.get('page', 1, type=int)
        count_per_page = request.args.get('count_per_page', 10, type=int)
        wx_date = request.args.get('wx_date', None)
        wx_year = request.args.get('wx_year', None)
        wx_station = request.args.get('wx_station', None)
        offset = (page-1) * count_per_page
        db_cursor = get_db_cursor()
        where_clause = "1=1"
        if wx_date:
            where_clause += f" and wx_date={wx_date}"
        if wx_year:
            where_clause += f" and wx_year={wx_year}"
        if wx_station:
            where_clause += f" and wx_station='{wx_station}'"
        db_cursor.execute(f"SELECT * FROM wx_data where {where_clause} limit {count_per_page} offset {offset}")
        rows = db_cursor.fetchall()

        # convert row objects to dictionary
        for i in rows:
            wx_data.append({
                "wx_station": i["wx_station"],
                "wx_date": i["wx_date"],
                "temp_max": i["temp_max"],
                "temp_min": i["temp_min"],
                "precipitation": i["precipitation"],
            })
    except Exception as ex:
        print(ex)
        wx_data = []
    return jsonify(wx_data)


@app.route('/api/yield')
def get_yield():
    yld_data = []
    try:
        page = request.args.get('page', 1, type=int)
        count_per_page = request.args.get('count_per_page', 10, type=int)
        yld_year = request.args.get('yld_year', None)
        offset = (page-1) * count_per_page
        db_cursor = get_db_cursor()
        where_clause = "1=1"
        if yld_year:
            where_clause += f" and yld_year={yld_year}"
        db_cursor.execute(f"SELECT * FROM corn_yield where {where_clause} limit {count_per_page} offset {offset}")
        rows = db_cursor.fetchall()

        # convert row objects to dictionary
        for i in rows:
            yld_data.append({
                "yield": i["yield"],
                "yld_year": i["yld_year"],
            })
    except Exception as ex:
        print(ex)
        yld_data = []
    return jsonify(yld_data)


@app.route('/api/weather/stats')
def get_weather_stats():
    wx_data = []
    try:
        page = request.args.get('page', 1, type=int)
        count_per_page = request.args.get('count_per_page', 10, type=int)
        wx_year = request.args.get('wx_year', None)
        wx_station = request.args.get('wx_station', None)
        offset = (page-1) * count_per_page
        db_cursor = get_db_cursor()
        where_clause = "1=1"
        if wx_year:
            where_clause += f" and wx_year={wx_year}"
        if wx_station:
            where_clause += f" and wx_station='{wx_station}'"
        db_cursor.execute(f"SELECT * FROM wx_avg_data_yearly where {where_clause} limit {count_per_page} offset {offset}")
        rows = db_cursor.fetchall()

        # convert row objects to dictionary
        for i in rows:
            wx_data.append({
                "wx_station": i["wx_station"],
                "wx_year": i["wx_year"],
                "temp_max_avg_yearly": i["temp_max_avg_yearly"],
                "temp_min_avg_yearly": i["temp_min_avg_yearly"],
                "precipitation_avg_yearly": i["precipitation_avg_yearly"],
            })
    except Exception as ex:
        print(ex)
        wx_data = []
    return jsonify(wx_data)


if __name__ == '__main__':
    app.run(port=5001)
