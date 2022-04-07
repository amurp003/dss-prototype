# this app uses FastAPI to ensure OpenAPI and JSON compliant interfaces
# https://fastapi.tiangolo.com
# default port is 3200

from fastapi import FastAPI

app = FastAPI()

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
      "1232": {
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
      "2365": {
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

@app.get("/")
def index():
    """
    This application returns tracks held within the Decision Support
    System (DSS). The field definitions align with definitions from 
    the OpenSky Network API.  
    https://openskynetwork.github.io/opensky-api/rest.html
    
    Go to '/docs' or '/redocs' to see the API documentation.
    """
    
    str = "Go to '/docs' or '/redocs' to see API documentation."
    return str

@app.get("/sensor_tracks")
def provide_sensor_tracks():
    """
    Returns sensor tracks held within the Decision Support
    System (DSS).
    
    This function simply provides the current sensor_tracks
    dictionary. Field definitions align with definitions from 
    the OpenSky Network API.  
    https://openskynetwork.github.io/opensky-api/rest.html
    
    Parameters
    ----------
    None.
    
    Returns
    -------
    icao24 (str) :
        Unique ICAO 24-bit address of the transponder 
        in hex string representation.
    
    callsign (str) :
        Callsign of the vehicle (8 chars). Can be null
        if no callsign has been received.
        
    origin_country (str) :
        Country name inferred from ICAO 24-bit address.
    
    last_contact (int) :
        Unix timestamp (seconds) for the last update in
        general. This field is updated for any new, valid
        message recieved from the transponder.
        
    longitude (float) :
        WGS-84 longitude in decimal degrees. Can be null.
        
    latitude (float) :
        WGS-84 latitude in decimal degrees. Can be null.
        
    baro_altitude (float) :
        Barometric altitude in **meters**. Can be null.
        
    velocity (float) :
        Velocity over ground in **m/s**. Can be null.
        
    true_track (float) :
        True track in decimal degrees clockwise from north
        (north=0°). Can be null.
        
    vertical_rate (float) :
        Vertical rate in **m/s**. A positive value indicates
        that the airplane is climbing, a negative value
        indicates that it descends. Can be null.
        
    squawk (str) :
        The transponder code aka Squawk. Can be null.
    """
    return sensor_tracks

@app.get("/system_tracks")
def provide_system_tracks():
    """
    Returns system tracks held within the Decision Support
    System (DSS).
    
    This function simply provides the current system_tracks
    dictionary. Field definitions align with definitions from 
    the OpenSky Network API. Additional definitions added to
    reflect translation of source data in English units.
    https://openskynetwork.github.io/opensky-api/rest.html
    
    Parameters
    ----------
    None.
    
    Returns
    -------
    icao24 (str) :
        Unique ICAO 24-bit address of the transponder 
        in hex string representation.
    
    callsign (str) :
        Callsign of the vehicle (8 chars). Can be null
        if no callsign has been received.
        
    origin_country (str) :
        Country name inferred from ICAO 24-bit address.
        
    last_contact (int) :
        Unix timestamp (seconds) for the last update in
        general. This field is updated for any new, valid
        message recieved from the transponder.
                
    bearing (float) :
        Bearing in decimal degrees from the local reference point 
        (e.g. airport location) clockwise from north (north=0°).
        Can be null.
        
    range (float) :
        Range in **nautical miles** (from the local reference point 
        (e.g. airport location). 1 nmi = 6076 feet.
        Can be null.
    
    elevation (float) :
        Range in **feet** (from the local reference point 
        (e.g. airport location). Can be null.
    
    longitude (float) :
        WGS-84 longitude in decimal degrees. Can be null.
        
    latitude (float) :
        WGS-84 latitude in decimal degrees. Can be null.
        
    baro_altitude (float) :
        Barometric altitude in **feet**. Can be null.
        
    velocity (float) :
        Velocity over ground in **knots**. Can be null.
        
    vertical_rate (float) :
        Vertical rate in **knots**. A positive value indicates
        that the airplane is climbing, a negative value
        indicates that it descends. Can be null.
        
    squawk (str) :
        The transponder code aka Squawk. Can be null.
    """
    return system_tracks
