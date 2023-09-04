from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import requests
import os
import psycopg2
import logging


logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s')


app = Flask(__name__, static_folder="./static", template_folder="./templates")


CORS(app)

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
        

        start = arrow.now().floor('day')
        end = arrow.now().ceil('day')
        response = requests.get(
            'https://api.stormglass.io/v2/weather/point',
            params={
                'lat': lat,
                'lng': lon,
                'params': ','.join(['waveHeight', 'airTemperature']),
                'start': start.to('UTC').timestamp(),  # Convert to UTC timestamp
                'end': end.to('UTC').timestamp()  # Convert to UTC timestamp
            },
            headers={
                'Authorization': api_key
            }
        )
        if response.status_code != 200:
            logging.error(f"Failed to fetch data from Stormglass API. Status code: {response.status_code}")
            return jsonify({"error": "Failed to fetch data from API."}), response.status_code
        

        data = response.json()
        temp = data['hours'][0]['airTemperature'].get('noaa')
        if not temp:
            temp = data['hours'][0]['airTemperature'].get('smhi')
        wave_height = data['hours'][0]['waveHeight'].get('noaa')
        if not wave_height:
            wave_height = data['hours'][0]['waveHeight'].get('meteo')
        save_to_db(lat, lon, temp, wave_height, None)  
        
        return jsonify(response.json()), 200

    except Exception as e:
        logging.error(f"Error fetching data for coordinates: lat={lat}, lon={lon}. Error: {e}")
        return jsonify({"error": "An error occurred while fetching data."}), 500

if __name__ == "__main__":
    create_table()
    app.run(host='0.0.0.0', port=5000, debug=True)

