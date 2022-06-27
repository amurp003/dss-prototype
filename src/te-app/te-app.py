from fastapi import FastAPI

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

trace.set_tracer_provider(
   TracerProvider(
       resource=Resource.create({SERVICE_NAME: "trial-engage-app"})
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
    title="te-app",
    description="Trial Engage Application",
)

# tm_url = "http://tm-server:3200/system_tracks"


resp_a = {"TN": "1232", 
            "Range": 25,
            "Type": "Type-C",
            "OptEval": 2}
    
resp_b = {"TN": "3242",
            "Range": 100, 
            "Type": "N/A",
            "OptEval": 1}

resp_c = {"TN": "2367",
            "Range": 74, 
            "Type": "N/A",
            "OptEval": 1}
       
resp_d = {"TN": "2453",
            "Range": 76,
            "Type": "Type-C",
            "OptEval": 1}
    
resp_e = {"TN": "2453",
            "Range": 72,
            "Type": "Type-B",
            "OptEval": 1}  

@app.get("/")
def readme():
    return {"te-ap": "The Threat Evaluation App is alive."}


@app.get("/unit_test/")
def trial_engage():
    """
    TE = Trial Engagement AI Service. Determines the lethality of a particular
    weapon against the track with subject TN. This version of the services
    operates standalone and does not make external calls.
    
    Parameters
    ----------
    None.
    
    Returns
    -------

    TN (octal) : 
        TN Integer in Octal. Assume octal at this time to ensure compatibility 
        with existing systems and TDL standards that have not evolved away from octal.

    Range (float) : 
        NM Range from ownship reference point to subject TN in nautical miles.

    Type (str) : 
        Identifies the weapon being using for trail engage assessment.

    OptRvd (int) : 
        Total number of options evaluated while determining a solution. This can 
        provide an indication of processing complexity. Multiple TE options indicates
        multiple intercept profiles.
    """
    with tracer.start_as_current_span("trial_eng") as span:
        span.set_attribute("response", resp_a)
        return resp_a

@app.get("/prod/")
def trial_engage():
    """
    TE = Trial Engagement AI Service. Determines the lethality of a particular
    weapon against the track with subject TN. This version of the services
    operates standalone and does not make external calls.
    
    Parameters
    ----------
    None.
    
    Returns
    -------

    TN (octal) : 
        TN Integer in Octal. Assume octal at this time to ensure compatibility 
        with existing systems and TDL standards that have not evolved away from octal.

    Range (float) : 
        NM Range from ownship reference point to subject TN in nautical miles.

    Type (str) : 
        Identifies the weapon being using for trail engage assessment.

    OptRvd (int) : 
        Total number of options evaluated while determining a solution. This can 
        provide an indication of processing complexity. Multiple TE options indicates
        multiple intercept profiles.
    """
    
    # assume that track kinematics are in the request and not request track data
    # tracks = requests.get(tm_url)
    # tracks_json = tracks.json()

    # return resp_a, tracks_json
    with tracer.start_as_current_span("trial_eng") as span:
        span.set_attribute("response", resp_a)
        return resp_a
    
FastAPIInstrumentor.instrument_app(app)
    