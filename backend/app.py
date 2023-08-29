from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from the backend!"

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city', default='Christchurch')  # Default city is Christchurch
    api_key = os.environ.get('OPENWEATHER_API_KEY')
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0')


