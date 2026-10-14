from dataclasses import dataclass

import requests
import json
import sqlite3
import time

DB_FILE = "database.db"

@dataclass
class TH:
    temp: float
    humidity : float

    def __init__(self, temp: str, humidity: str):
        try:
            self.temp = float(temp)
            self.humidity = float(humidity)
        except ValueError:
            self.temp = float("0")
            self.humidity = float("0")
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("insert into errors (error) VALUES (?)",
                                "There was an error parsing data from one of the endpoints"
                            )
            conn.commit()

def initialiseDB():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS TH (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bme_temp REAL NOT NULL,
        bme_humidity REAL NOT NULL,
        meteo_temp REAL NOT NULL,
        meteo_humidity REAL NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
""")
    conn.commit()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS errors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            error TEXT NOT NULL
        )
    """)
    conn.commit()

def get_bme_data() -> TH:
    response = requests.get("<ADD SENSOR URL>")
    data = json.loads(response.content)
    return TH(data['temperature'], data['humidity'])

def get_meteo_data() -> TH:
    base_url = "https://api.open-meteo.com/v1/forecast"
    response = requests.get(base_url,
                 params={
                    "latitude":"<Add latitude>",
                    "longitude":"<Add longitude>",
                    "timezone":"Australia/Sydney",
                    "current":"temperature_2m,relative_humidity_2m"
                 })
    data = json.loads(response.content)
    return TH(data['current']['temperature_2m'], data['current']['relative_humidity_2m'])

def write_entry(bme: TH,meteo: TH) -> None:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("insert into TH (bme_temp, bme_humidity, meteo_temp, meteo_humidity) VALUES (?, ?, ?, ?)",(
        bme.temp,
        bme.humidity,
        meteo.temp,
        meteo.humidity
    ))
    conn.commit()

if __name__ == '__main__':
    initialiseDB()
    while True:
        bme = get_bme_data()
        meteo = get_meteo_data()
        write_entry(bme, meteo)
        print("Added entry to database")
        print("Printing DB")
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("select * from TH")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        time.sleep(300)

