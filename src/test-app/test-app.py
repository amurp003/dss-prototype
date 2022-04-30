# this app uses FastAPI to ensure OpenAPI and JSON compliant interfaces
# https://fastapi.tiangolo.com
# default port is 3200

# https://www.geeksforgeeks.org/http-request-methods-python-requests/
# https://docs.python-requests.org/en/latest/api/
# pip3 install requests

import requests
import time
from datetime import datetime
from fastapi import FastAPI

# opentelemetry libraries
from opentelemetry import trace

# bring in automatic tracing of FastAPI operations and Requests
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# export traces to Jaeger
# https://opentelemetry-python.readthedocs.io/en/latest/exporter/jaeger/jaeger.html
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# add opentelemetry propogator code
# from opentelemetry.propagate import set_global_textmap
# from opentelemetry.propagators.b3 import B3Format

# set_global_textmap(B3Format())

trace.set_tracer_provider(
   TracerProvider(
       resource=Resource.create({SERVICE_NAME: "dss-automated-test"})
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


app = FastAPI()

tm_url = "http://tm-server:3200/system_tracks"

# set default values
num_tests = 5      # consider 50
num_requests = 5   # number of local requests per test; e.g. 10
request_delay = 1   # seconds to wait before sending a request
                    # to avoid collisions
                    
@app.get("/")
def index():
    """
    This application provides automated testing within the
    Decision Support System (DSS). Go to '/docs' or 'redocs'
    to see the API documention.
    """
    
    str = "Go to '/docs' or '/redocs' to see API documentation."
    return str

@app.get("/test-tm/")
def tm_test():
    
    tracks = requests.get(tm_url)
    tracks_json = tracks.json()
    return tracks_json


@app.get("/test/")
def run_tests(num_tests: int = 5, num_requests: int = 5,
                    request_delay: int = 1):
    
    print ("Starting tests ...")

    # time in UTC
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for test in range(0, num_tests):
        
        with tracer.start_as_current_span("start test"):
                        
            for serviceRqst in range(0, num_requests):

                # request IAD flight data
                time.sleep(request_delay)
                with tracer.start_as_current_span("test: RIC"):
                    requests.get('http://dss-ui:5000/RIC')
    
                # request RIC flight data
                time.sleep(request_delay)
                with tracer.start_as_current_span("test: IAD"):
                    requests.get('http://dss-ui:5000/IAD')                
                
                # request track data via dss-ui
                time.sleep(request_delay)
                with tracer.start_as_current_span("test: tracks"):
                    requests.get('http://dss-ui:5000/tracks')
            
                # request trial engage via dss-ui
                time.sleep(request_delay)
                with tracer.start_as_current_span("test: TE"):
                    requests.get('http://dss-ui:5000/TE')

                # request wpn assessment
                time.sleep(request_delay)
                with tracer.start_as_current_span("test: WA"):
                    requests.get('http://dss-ui:5000/WA')
            
                print(f"     sub-test {(serviceRqst+1)} of \
                    {num_requests} complete ...")
        
            print(f"Test {(test+1)}  of {num_tests} complete ...")

    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    test_parameters = [{
        "num_tests": str(num_tests),
        "num_requests": str(num_requests),
        "request_delay": str(request_delay),
        "start_time": str(start_time),
        "end_time": str(end_time)
        }]
    
    return test_parameters