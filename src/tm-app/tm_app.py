from flask import Flask, make_response, jsonify

app = Flask(__name__)

PORT = 3200
HOST = '0.0.0.0'

# set initial track data using OpenSky API definitions
# https://openskynetwork.github.io/opensky-api/rest.html

# the dictionary key is the unique icao24 from the transponder
# this sample is from 1646806209 UTC
# Wed Mar 09 2022 01:10:09 GMT-0500 (EST)

sensor_tracks = {
     "a88e98": {
         "callsign" : "N650VC  ",
         "origin_country" : "United States",
         "last_contact" : "1646806209",
         "latitude" : "-76.9576",
         "longitude" : "39.3062",
         "baro_altitude" : "1447.8",
         "velocity" : "146.46",
         "true_track" : "67.49",
         "vertical_rate" : "-0.33",
         "squawk" : "4655",
     },
       "a1c57e": {
         "callsign" : "RPA5631 ",
         "origin_country" : "United States",
         "last_contact" : "1646806209",
         "latitude" : "-77.4533",
         "longitude" : "38.9482",
         "baro_altitude" : "null",
         "velocity" : "2.83",
         "true_track" : "0",
         "vertical_rate" : "null",
         "squawk" : "2714",
     },
      "a21f04": {
         "callsign" : "GTX511  ",
         "origin_country" : "United States",
         "last_contact" : "1646806209",
         "latitude" : "-76.4866",
         "longitude" : "38.9715",
         "baro_altitude" : "1158.24",
         "velocity" : "74.99",
         "true_track" : "157.83",
         "vertical_rate" : "0",
         "squawk" : "2115",
     },
      "e08443": {
         "callsign" : "LVHQC   ",
         "origin_country" : "Argentina",
         "last_contact" : "1646806209",
         "latitude" : "-76.4663",
         "longitude" : "38.589",
         "baro_altitude" : "2054.84",
         "velocity" : "261.42",
         "true_track" : "22.93",
         "vertical_rate" : "-14.63",
         "squawk" : "5244",
     }      
}
# this should use common data model naming conventions
system_tracks = {
      "1237": {
         "icao24" : "a88e98",
         "callsign" : "",
         "origin_country" : "",
         "last_contact" : "",
         "bearing" : "",
         "range" : "",
         "elevation" : "",
         "latitude" : "",
         "longitude" : "",
         "baro_altitude" : "",
         "velocity" : "",
         "vertical_rate" : "",
         "squawk" : "",
     },
      "5235": {
         "icao24" : "e08443",
         "callsign" : "LVHQC   ",
         "origin_country" : "Argentina",
         "bearing" : "",
         "range" : "",
         "elevation" : "",
         "last_contact" : "",
         "latitude" : "",
         "longitude" : "",
         "baro_altitude" : "",
         "velocity" : "",
         "vertical_rate" : "",
         "squawk" : "",
      }
}

@app.route('/')
def index():
    return '<h1>Track Management Service [tm-app] is running...</h1>'

@app.route('/sensor_tracks')
def provide_sensor_tracks():
    res = make_response(jsonify(sensor_tracks,200))
    return res

@app.route('/system_tracks')
def provide_system_tracks():
    res = make_response(jsonify(system_tracks,200))
    return res

# always at the end to start server and keep things running
if __name__ == "__main__":
    # message to terminal
    print("TM Service running on port %s" %(PORT))
    app.run(debug=True, host=HOST, port=PORT)