from flask import Flask, render_template, request, Response, abort, redirect
import urllib.parse
import json
import time

from datetime import datetime
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route('/weather', methods=['GET', 'POST'])
def get_weather():
    city = request.form['city']
    if city is None:
        abort(400, 'Missing argument city')
    data = {}

    data['q'] = city
    data['appid'] = '475e3a0d142dd7a2580f0374834f4a23'
    data['units'] = 'metric'
    url_values = urllib.parse.urlencode(data)

    url = 'http://api.openweathermap.org/data/2.5/weather?'
    full_url = url+url_values
    print(full_url)
    data = urllib.request.urlopen(full_url)
    data2 = urllib.request.urlopen(full_url)

    resp = Response(data)

    resp.status_code = 200
    data2 = json.loads(data2.read().decode('utf8'))

    lat = data2['coord']['lat']
    lon = data2['coord']['lon']

    time_url = 'https://timeapi.io/api/Time/current/coordinate?latitude=' + \
        str(lat)+'&longitude='+str(lon)
    timeCity = urllib.request.urlopen(time_url)
    dateCity = urllib.request.urlopen(time_url)

    return render_template('weather.html', title='Weather App', date=json.loads(dateCity.read().decode('utf8')), time=json.loads(timeCity.read().decode('utf8')), data=json.loads(data.read().decode('utf8')))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
