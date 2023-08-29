from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from the backend!"

@app.route('/surfcast', methods=['GET'])
def get_surfcast():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    api_key = os.environ.get('STORMGLASS_API_KEY')

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
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0')


