from typing import Optional

from fastapi import FastAPI
import requests

app = FastAPI()

tm_url = "http://tm-server:3200/system_tracks"

resp_a = {"TN": "1232",
              "Range": 27,
              "Type": "Type-C, Type-D",
              "OptEval": 3}
    
resp_b = {"TN": "2365",
              "Range": 100,
              "Type": "N/A",
              "OptEval": 2}

resp_c = {"TN": "2365",
              "Range": 80,
              "Type": "Type-A",
              "OptEval": 4}
     
resp_d = {"TN": "2453",
              "Range": 83,
              "Type": "Type-B, Type-C",
              "OptEval": 4}
    
resp_e = {"TN": "2453",
              "Range": 81,
              "Type": "Type-B, Type-C",
              "OptEval": 3}

@app.get("/")
def readme():
    return {"wa-app": "The Weapon Assessment App is alive."}


@app.get("/unit-test/")
def wpn_assmt():
    """
    WA = Weapon Assessment AI Service. Determines what weapons have
    capability against the track with subject TN. This is the standalone
    version of the service.

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
        Provides a list of weapons with an interceptability solution.
    
    OptRvd (int) : 
        Total number of options evaluated while determining a solution. This can 
        provide an indication of processing complexity. 
    """

    return resp_a

@app.get("/prod/")
def wpn_assmt():
    """
    WA = Weapon Assessment AI Service. Determines what weapons have
    capability against the track with subject TN. This service requires
    the track management container.

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
        Provides a list of weapons with an interceptability solution.
    
    OptRvd (int) : 
        Total number of options evaluated while determining a solution. This can 
        provide an indication of processing complexity. 
    """

    tracks = requests.get(tm_url)
    tracks_json = tracks.json()

    return resp_a, tracks_json