from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import requests
import os
import psycopg2
import logging


logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s')


app = Flask(__name__, static_folder="./static", template_folder="./templates")


CORS(app, resources={r"/surfcast/*": {"origins": "http://localhost:8080"}})

DATABASE_CONFIG = {
    'dbname': 'weather',
    'user': 'user',         
    'password': 'password', 
    'host': 'db',
    'port': '5432' 
}


def get_db_connection():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    return conn

def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        '''
CREATE TABLE IF NOT EXISTS surf_data (
    id SERIAL PRIMARY KEY,
    lat FLOAT NOT NULL,
    lon FLOAT NOT NULL,
    waveHeight FLOAT,
    wind FLOAT,
    swell FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
        '''
    )
    conn.commit()
    cur.close()
    conn.close()

def save_to_db(lat, lon, waveHeight, wind, swell):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO surf_data (lat, lon, waveHeight, wind, swell) VALUES (%s, %s, %s, %s, %s)",
        (lat, lon, waveHeight, wind, swell)
    )
    conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')  

@app.route('/surfcast', methods=['GET'])
def surfcast():
    try:
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        
        if not lat or not lon:
            return jsonify({"error": "Both latitude and longitude are required."}), 400

        try:
            lat = float(lat)
            lon = float(lon)
        except ValueError:
            return jsonify({"error": "Latitude and longitude must be valid numbers."}), 400
        
        logging.info(f"Fetching data for coordinates: lat={lat}, lon={lon}")
        
        api_key = os.environ.get('STORMGLASS_API_KEY')
        if not api_key:
            logging.warning("STORMGLASS_API_KEY not set. Cannot fetch data.")
            return jsonify({"error": "API key not set."}), 500
        
        response = requests.get(f"https://api.stormglass.io/v2/weather/point?lat={lat}&lon={lon}", headers={"Authorization": api_key})
        if response.status_code != 200:
            logging.error(f"Failed to fetch data from Stormglass API. Status code: {response.status_code}")
            return jsonify({"error": "Failed to fetch data from API."}), response.status_code
        
        data = response.json()
        temp = data['hours'][0]['airTemperature']['noaa']
        wind_speed = data['hours'][0]['windSpeed']['noaa']
        wind_dir = data['hours'][0]['windDirection']['noaa']
        save_to_db(lat, lon, temp, wind_speed, wind_dir)
        
        return jsonify(response.json()), 200

    except Exception as e:
        logging.error(f"Error fetching data for coordinates: lat={lat}, lon={lon}. Error: {e}")
        return jsonify({"error": "An error occurred while fetching data."}), 500

if __name__ == "__main__":
    create_table()
    app.run(host='0.0.0.0', port=5000)