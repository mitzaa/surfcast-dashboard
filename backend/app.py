from flask import Flask, jsonify, request, render_template
import requests
import os
import psycopg2

app = Flask(__name__, 
            static_folder='frontend/static', 
            template_folder='frontend/templates')

DATABASE_CONFIG = {
    'dbname': 'weather',
    'user': 'marion',
    'password': 'surfcast',
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

@app.route('/surfcast/', methods=['GET'])
def get_surfcast():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    api_key = os.environ.get('STORMGLASS_API_KEY')

    if not lat or not lon:
        return jsonify({"error": "Please provide both lat and lon parameters."}), 400

    params = ','.join([
        'waveHeight', 'waveDirection', 'wavePeriod', 
        'windSpeed', 'windDirection', 'airTemperature',
        'swellHeight', 'swellDirection', 'swellPeriod'
    ])
    
    url = f"https://api.stormglass.io/v2/weather/point?lat={lat}&lng={lon}&params={params}"
    
    headers = {
        'Authorization': api_key
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data from Stormglass API."}), 500
    
    data = response.json()
    
    waveHeight = data.get('waveHeight')
    wind = data.get('windSpeed')
    swell = data.get('swellHeight')

    save_to_db(lat, lon, waveHeight, wind, swell)
    print(response.status_code)
    print(response.json())

    
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0')






