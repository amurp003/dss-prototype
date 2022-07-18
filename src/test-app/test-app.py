# this app uses FastAPI to ensure OpenAPI and JSON compliant interfaces

import requests
import time
from datetime import datetime
from fastapi import FastAPI
import psutil

# opentelemetry libraries
from opentelemetry import trace

# bring in automatic tracing of FastAPI operations and Requests
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# export traces to Jaeger
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# changed the services name
trace.set_tracer_provider(
   TracerProvider(
       resource=Resource.create({SERVICE_NAME: "DSS-test-app"})
   )
)

jaeger_exporter = JaegerExporter(
#    agent_host_name="localhost",
   agent_host_name="telem-jaeger",
   agent_port=6831,
)

trace.get_tracer_provider().add_span_processor(
   BatchSpanProcessor(jaeger_exporter)
)

tracer = trace.get_tracer(__name__)
span = trace.get_current_span()


app = FastAPI(
    title="test-app",
    description="DSS automated test application",
)

tm_url = "http://tm-server:3200/system_tracks"

# set default values
num_tests = 5      # consider 5
num_requests = 5   # number of local requests per test; e.g. 5
request_delay = 1   # seconds to wait before sending a request
                    # to avoid collisions; e.g. 1
                    
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
            
            span = trace.get_current_span()
            
            # log compute metrics
            loadavg = psutil.getloadavg()
            numcpu = psutil.cpu_count()
            net_io_count = psutil.net_io_counters()
            
            span.set_attribute("cpu.load.avg", loadavg)
            span.set_attribute("num.cpu", numcpu)
            span.set_attribute("net.io.count", net_io_count)
            span.add_event( "start test", {
                "test.number": (test + 1),
                "num.tests": num_tests,
                "request.delay": request_delay,
            })
                        
            for serviceRqst in range(0, num_requests):

                # request RIC flight data
                time.sleep(request_delay)
                with tracer.start_as_current_span("RIC") as child:
                    
                    span = trace.get_current_span()
                    
                    net_io_count = psutil.net_io_counters()
                    
                    requests.get('http://dss-ui:5000/RIC')
                    
                    addio = psutil.net_io_counters()
                    span.set_attribute("start.io.count", net_io_count)
                    span.set_attribute("end.io.count", addio)
    
                # request IAD flight data
                time.sleep(request_delay)
                with tracer.start_as_current_span("IAD")as child:
                    
                    span = trace.get_current_span()
                    net_io_count = psutil.net_io_counters()
                    
                    requests.get('http://dss-ui:5000/IAD') 
                    
                    addio = psutil.net_io_counters()
                    span.set_attribute("start.io.count", net_io_count)
                    span.set_attribute("end.io.count", addio)                                   
                
                # request track data via dss-ui
                time.sleep(request_delay)
                with tracer.start_as_current_span("tracks") as child:
                    
                    span = trace.get_current_span()
                    net_io_count = psutil.net_io_counters()
                                    
                    requests.get('http://dss-ui:5000/tracks')
                    
                    addio = psutil.net_io_counters()
                    span.set_attribute("start.io.count", net_io_count)
                    span.set_attribute("end.io.count", addio) 
            
                # request trial engage via dss-ui
                time.sleep(request_delay)
                with tracer.start_as_current_span("Trial-Eng") as child:
                    
                    span = trace.get_current_span()
                    net_io_count = psutil.net_io_counters()
                
                    requests.get('http://dss-ui:5000/TE')
                    
                    addio = psutil.net_io_counters()
                    span.set_attribute("start.io.count", net_io_count)
                    span.set_attribute("end.io.count", addio) 

                # request wpn assessment
                time.sleep(request_delay)
                with tracer.start_as_current_span("Wpn-Assmt") as child:
                    
                    span = trace.get_current_span()
                    net_io_count = psutil.net_io_counters()
                    
                    requests.get('http://dss-ui:5000/WA')
                    
                    addio = psutil.net_io_counters()
                    span.set_attribute("start.io.count", net_io_count)
                    span.set_attribute("end.io.count", addio)
                    
            span.end()
            
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