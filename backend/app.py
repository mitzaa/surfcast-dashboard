from flask import Flask, jsonify, request, render_template
import requests
import os

app = Flask(__name__, 
            static_folder='frontend/static', 
            template_folder='frontend/templates')

@app.route('/')
def index():
    return render_template('index.html')  

@app.route('/surfcast', methods=['GET'])
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
    
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0')



