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
       resource=Resource.create({SERVICE_NAME: "DSS-test-app"})
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


app = FastAPI(
    title="test-app",
    description="DSS automated test application",
)

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
    """
    This endpoint merely requests track data from the tm-app and outputs
    the response.
    """
    
    tracks = requests.get(tm_url)
    tracks_json = tracks.json()
    return tracks_json


@app.get("/test/")
def run_tests(num_tests: int = 5, num_requests: int = 5,
                    request_delay: int = 1):
    """
    This endpoint runs a series of automated tests based upon user
    supplied number of tests, number of requests, and a request
    delay.
    
    Parameters
    ----------
    num_tests (int) :   
       Number of tests to run.
    
    num_requests (int) :
        Number of request cycles within each test. Each cycle consists of:  
            *1. Request Dulles (IAD) flight data*  
            *2. Request Richmond (RIC) flight data*  
            *3. Request local tracks*  
            *4. Request trial engagement*  
            *5. Request weapon assessment*   
    
    request_delay (int) :
        Delay between request in seconds to avoid overloading internal
        and external servers.
    
    Returns
    -------
    num_tests (str) :  
        Converted string. See parameters above.
        
    num_requests (str) :  
        Converted string. See parameters above.
        
    request_delay (str) :  
        Converted string. See parameters above.
        
    start_time (str) :  
        Test start time in GMT; e.g. "2022-06-06 23:21:26"
    
    end_time (str) :  
        Test end time in GMT; e.g. "2022-06-06 23:21:59"
    """
   
    print ("Starting tests ...")

    # time in UTC
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for test in range(0, num_tests):
        
        with tracer.start_as_current_span("start-test") as span:
            
            current_span = trace.get_current_span()
                        
            for serviceRqst in range(0, num_requests):

                # request IAD flight data
                time.sleep(request_delay)
                with tracer.start_as_current_span("RIC") as child:
                    requests.get('http://dss-ui:5000/RIC')
                    current_span.set_attribute("operation.value", 1)
    
                # request RIC flight data
                time.sleep(request_delay)
                with tracer.start_as_current_span("IAD")as child:
                    requests.get('http://dss-ui:5000/IAD')                
                
                # request track data via dss-ui
                time.sleep(request_delay)
                with tracer.start_as_current_span("tracks") as child:
                    requests.get('http://dss-ui:5000/tracks')
            
                # request trial engage via dss-ui
                time.sleep(request_delay)
                with tracer.start_as_current_span("Trial-Eng")as child:
                    requests.get('http://dss-ui:5000/TE')

                # request wpn assessment
                time.sleep(request_delay)
                with tracer.start_as_current_span("Wpn-Assmt") as child:
                    requests.get('http://dss-ui:5000/WA')
            
            #     print(f"     sub-test {(serviceRqst+1)} of \
            #         {num_requests} complete ...")
        
            # print(f"Test {(test+1)}  of {num_tests} complete ...")

    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    test_parameters = [{
        "num_tests": str(num_tests),
        "num_requests": str(num_requests),
        "request_delay": str(request_delay),
        "start_time": str(start_time),
        "end_time": str(end_time)
        }]
    
    return test_parameters