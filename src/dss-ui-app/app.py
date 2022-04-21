# attempting to send traces to Jaegar

# flask Libraries
import flask
import requests # https://realpython.com/api-integration-in-python/
from flask import render_template

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
        resource=Resource.create({SERVICE_NAME: "dss-prototype"})
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


app = flask.Flask(__name__)

# Capture Flask operations
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

        url_RIC = "http://tm-server:3200/track-init/RIC"
   
        api_url = url_RIC
        response = requests.get(api_url)
        return (response.json())

@app.route('/IAD')
def get_iad_flights():
    with tracer.start_as_current_span("IAD Flight Data"):

        url_IAD = "http://tm-server:3200/track-init/IAD"

        api_url = url_IAD
        response = requests.get(api_url)
        return (response.json())

@app.route('/tracks')
def get_system_tracks():
    with tracer.start_as_current_span("TM Track Update"):

        url_TM = "http://tm-server:3200/system_tracks"
        api_url = url_TM
        response = requests.get(api_url)
        return (response.json())

@app.route('/TE')
def trial_engage():
    with tracer.start_as_current_span("Trial Engage"):

        url_TE = "http://te-app:3202/prod"
        api_url = url_TE
        response = requests.get(api_url)
        return (response.json())

@app.route('/WA')
def weapon_assmt():
    with tracer.start_as_current_span("Weapon Assmt"):

        url_WA = "http://wa-app:3201/prod"
        api_url = url_WA
        response = requests.get(api_url)
        return (response.json())
        
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
