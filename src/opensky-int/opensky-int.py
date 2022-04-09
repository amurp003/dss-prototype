# this app uses FastAPI to ensure OpenAPI and JSON compliant interfaces
# https://fastapi.tiangolo.com
# default port is 3200

from fastapi import FastAPI

import requests # https://realpython.com/api-integration-in-python/

# set initial track data using OpenSky API definitions
# https://openskynetwork.github.io/opensky-api/rest.html



# opentelemetry libraries 
from opentelemetry import trace

# Next 2 lines bring in automatic tracing of Flask operations
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

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

app = FastAPI()

# Capture Flask operations
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

tracer = trace.get_tracer(__name__)

@app.get("/")
def index():
    """
    This application get "sensor" track data from the OpenSky API. 
    The field definitions align with definitions from 
    the OpenSky Network API.  
    https://openskynetwork.github.io/opensky-api/rest.html
    
    Go to '/docs' or '/redocs' to see the API documentation.
    """   
    str = "Go to '/docs' or '/redocs' to see API documentation."
    return str

@app.get("/flights/{airport}")
def get_flights(airport: str, IAD):
    """
    Interfaces with the OpenSky API to return sensor track
    flight data. This function simply provides the current sensor_tracks
    dictionary. Field definitions align with definitions from 
    the OpenSky Network API.  
    https://openskynetwork.github.io/opensky-api/rest.html
    
    Parameters
    ----------
    None.
    
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
        
        with tracer.start_as_current_span("IAD Flight Data"):
        # Latitude = N/S, Longitude = E/W
        # 1 deg = 60 NM Lat, varies with Lon
        # N and E are positive

        # IAD 38.9531 N, 77.4565 W 

        url_IAD = "https://opensky-network.org/api/states/all?lamin=37.9537&lomin=-78.4565&lamax=39.9537&lomax=-76.4565"

        api_url = url_IAD
        flights = requests.get(api_url)
        
    elif airport == "RIC":
    
        with tracer.start_as_current_span("RIC Flight Data"):
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
        flights = requests.get(api_url)
        
    return flights.json()
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
