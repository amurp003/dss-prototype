from typing import Optional

from fastapi import FastAPI
import requests

app = FastAPI()

tm_url = "http://tm-server:3200/system_tracks"


resp_a = {"TN": "1232", 
            "Range": "25",
            "Type": "Type-C",
            "OptEval": "2"}
    
resp_b = {"TN": "3242",
            "Range": "100", 
            "Type": "N/A",
            "OptEval": "1"}

resp_c = {"TN": "2367",
            "Range": "74", 
            "Type": "N/A",
            "OptEval": "1"}
       
resp_d = {"TN": "2453",
            "Range": "76",
            "Type": "Type-C",
            "OptEval": "1"}
    
resp_e = {"TN": "2453",
            "Range": "72",
            "Type": "Type-B",
            "OptEval": "1"}  

@app.get("/")
def readme():
    return {"te-ap": "The Threat Evaluation App is alive."}


@app.get("/unit_test/")
def trial_engage():
    """
    WA = Weapon Assessment AI Service. Determines what weapons have
    capability against the track with subject TN. This version of the services
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
    
    return resp_a

@app.get("/prod/")
def trial_engage():
    """
    WA = Weapon Assessment AI Service. Determines what weapons have
    capability against the track with subject TN. This version of the services calls
    the track service before returning a response.
    
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
    
    tracks = requests.get(tm_url)
    tracks_json = tracks.json()

    return resp_a, tracks_json