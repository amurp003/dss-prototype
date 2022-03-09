# This version of the app reports spans to the terminal session
# See flask_example from 
# https://opentelemetry.io/docs/instrumentation/python/getting-started/

import flask
import requests # https://realpython.com/api-integration-in-python/
from flask import render_template

from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(ConsoleSpanExporter())
)

app = flask.Flask(__name__)

FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

tracer = trace.get_tracer(__name__)

@app.route('/')
def ui():
    with tracer.start_as_current_span("rendermap"):
        return render_template('leaflet-map-ui.html')

@app.route('/RIC')
def get_ric_flights():
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
        response = requests.get(api_url)
        return (response.json())

@app.route('/IAD')
def get_iad_flights():
    with tracer.start_as_current_span("IAD Flight Data"):
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