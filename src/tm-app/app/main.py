# this app uses FastAPI to ensure OpenAPI and JSON compliant interfaces
# https://fastapi.tiangolo.com
# default port is 3200

from fastapi import FastAPI
import requests # https://realpython.com/api-integration-in-python/

# opentelemetry libraries 
from opentelemetry import trace

# bring in automatic tracing of FastAPI operations
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from opentelemetry.instrumentation.requests import RequestsInstrumentor

# export traces to Jaeger
# https://opentelemetry-python.readthedocs.io/en/latest/exporter/jaeger/jaeger.html
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "opensky-interface"})
    )
)

# note that agent port is different from the webconsole port 16686
# localhost within a container refers to the container not the host running the container
# defined a container network and a alias for the telemetry container; e.g.
# docker run --network-alias=telem-jaeger --network=dss-net
# will need localhost (or other known endpoint) to test outside of the container

jaeger_exporter = JaegerExporter(
#    agent_host_name="localhost",
    agent_host_name="telem-jaeger",
    agent_port=6831,
)

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

tracer = trace.get_tracer(__name__)
current_span = trace.get_current_span()
ctx = trace.get_current_span().get_span_context()
link_from_current = trace.Link(ctx)

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

@app.get("/track-init/{airport}")
def get_flights(airport: str = {'IAD', 'RIC'}):
    """
    Interfaces with the TM App to establish OpenSky API connection
    for flight data. Field definitions align with definitions from 
    the OpenSky Network API.  
    https://openskynetwork.github.io/opensky-api/rest.html
    
    Parameters
    ----------
    airport (str) :   
        Either IAD or DCA to recieve contacts within 60 nmi of
        the selected airport.
    
    Returns
    -------
    icao24 (str) :  
        0 - Unique ICAO 24-bit address of the transponder 
        in hex string representation.
    
    callsign (str) :  
        1 - Callsign of the vehicle (8 chars). Can be null
        if no callsign has been received.
        
    origin_country (str) :  
        2 - Country name inferred from ICAO 24-bit address.
    
    time_position (int) :  
        3 - Unix timestamp (seconds) for the last position update. 
        Can be null if no position report was received by OpenSky 
        within the past 15s.
    
    last_contact (int) :  
        4 - Unix timestamp (seconds) for the last update in
        general. This field is updated for any new, valid
        message recieved from the transponder.
        
    longitude (float) :  
        5 - WGS-84 longitude in decimal degrees. Can be null.
        
    latitude (float) :  
        6 - WGS-84 latitude in decimal degrees. Can be null.
        
    baro_altitude (float) :  
        7 - Barometric altitude in **meters**. Can be null.
        
    on_ground(bool) :   
        8 - Boolean value which indicates if the position was retrieved from 
        a surface position report.
    
    velocity (float) :  
        9 - Velocity over ground in **m/s**. Can be null.
        
    true_track (float) :  
        10 - True track in decimal degrees clockwise from north
        (north=0°). Can be null.
        
    vertical_rate (float) :  
        11 - Vertical rate in **m/s**. A positive value indicates
        that the airplane is climbing, a negative value
        indicates that it descends. Can be null.
        
    sensors (int) :  
        12 - IDs of the receivers which contributed to this state vector.
        Is null if no filtering for sensor was used in the request.
    
    geo_altitude (float) :  
        13 - Geometric altitude in meters. Can be null.
    
    squawk (str) :  
        14 - The transponder code aka Squawk. Can be null.
        
    spi (bool) :  
        15 - Whether flight status indicates special purpose indicator.
        
    position_source (int) :  
        16 - Origin of this state’s position: 0 = ADS-B, 1 = ASTERIX, 2 = MLAT
    """
    
    if airport == "IAD":
        
        with tracer.start_as_current_span("IAD Source Tracks",
                                          links=[link_from_current]) as new_span:

            url_IAD = "http://opensky-int:3203/flights/IAD"
            
            api_url = url_IAD
            flights = requests.get(api_url).json()
        
    elif airport == "RIC":
    
        with tracer.start_as_current_span("RIC Source Tracks",
                                          links=[link_from_current]) as new_span:
        
            url_RIC = "http://opensky-int:3203/flights/RIC"
            
            api_url = url_RIC
            flights = requests.get(api_url).json()
            
    return flights
