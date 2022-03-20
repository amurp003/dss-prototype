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

app = FastAPI()

# set default values
num_tests = 5      # consider 10
num_requests = 5   # number of local requests per test; e.g. 50
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


@app.get("/test/")
async def run_tests(num_tests: int = 5, num_requests: int = 5,
                    request_delay: int = 1):
    
    print ("Starting tests ...")

    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for test in range(0, num_tests):

        # request IAD flight data
        time.sleep(request_delay)
        requests.get('http://localhost:3200/IAD')
    
        # request RIC flight data
        time.sleep(request_delay)
        requests.get('http://localhost:3200/RIC')
    
    for serviceRqst in range(0, num_requests):

        # request track data via dss-ui
        time.sleep(request_delay)
        requests.get('http://localhost:5000/tracks')
        
        print(f"     sub-test {(serviceRqst+1)} of \
                {num_requests} complete ...")
        
    print(f"Test {(test+1)}  of {num_tests} complete ...")

    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print("Tests complete.")
    print(f"Start time: {start_time}.")
    print(f"End time: {end_time}.")        
        
    return end_time