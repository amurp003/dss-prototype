# https://www.geeksforgeeks.org/http-request-methods-python-requests/
# https://docs.python-requests.org/en/latest/api/
# pip3 install requests

import requests
import time
from datetime import datetime

num_tests = 10

start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

for x in range(0, num_tests):

    # request track data via dss-ui
    requests.get('http://localhost:5000/tracks')

    time.sleep(3)
    
    # check status code for response received
    # success code - 200
    # print(r)

    # print content of request
    # print(r.content)

end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')    

print('Tests complete.')
print('Start time: %s' % start_time)
print('End time: %s' % end_time)

