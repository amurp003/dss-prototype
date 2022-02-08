from pickletools import uint1
from flask import Flask
from flask import render_template
import requests # https://realpython.com/api-integration-in-python/

app = Flask(__name__)

@app.route('/')
def ui():
    return render_template('leaflet-map-ui.html')

@app.route('/RIC')
def get_ric_flights():
    # Latitude = N/S, Longitude = E/W
    # 1 deg = 60 NM Lat, varies with Lon
    # N and E are positive

    #RIC 37.5407 N, 77.4360 W
    # Richmond box
    # lamin=37.5407 - 1 =36.5407
    # lomin=-77.4360 - 1=-78.4360 W
    # lamax=37.5407 + 1 = 38.5407 N
    # lomax=-77.4360 + 1 = -76.4360 W

    url_RIC = "https://opensky-network.org/api/states/all?lamin=36.5407&lomin=-78.4360&lamax=38.5407&lomax=-76.4360"
   
    api_url = url_RIC
    response = requests.get(api_url)
    return (response.json())

@app.route('/IAD')
def get_iad_flights():
    # Latitude = N/S, Longitude = E/W
    # 1 deg = 60 NM Lat, varies with Lon
    # N and E are positive

    # IAD 38.9531 N, 77.4565 W 

    url_IAD = "https://opensky-network.org/api/states/all?lamin=37.9537&lomin=-78.4565&lamax=39.9537&lomax=-76.4565"

    api_url = url_IAD
    response = requests.get(api_url)
    return (response.json())

if __name__ == "__main__":
    app.run(debug=True)
