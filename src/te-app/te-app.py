import requests
from typing import Optional

from opentelemetry import trace # do we want this
# from fastapi import FastAPI
tracer = trace.get_tracer(__name__) # do we want this

import fastapi
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from opentelemetry.exporter.jaeger.thrift import JaegerExporter
jaeger_exporter = JaegerExporter(
#    agent_host_name="localhost",
   agent_host_name="telem-jaeger",
   agent_port=6831,
)

app = fastapi.FastAPI(
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
    with tracer.start_as_current_span("trial_eng") as trial_engage_span:
        trial_engage_span.set_attribute("response", resp_a)
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
    with tracer.start_as_current_span("trial_eng") as trial_engage_span:
        trial_engage_span.set_attribute("response", resp_a)
        return resp_a
    
FastAPIInstrumentor.instrument_app(app)
    