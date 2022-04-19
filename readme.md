# Decision Support System (DSS) Microservices Project

The United States Department of Defense (DoD) is rapidly working with DoD Services to move from multi-year (e.g. 7-10) traditional acquisition programs to a commercial industry-based approach for software development. While commercial technologies and approaches provide an opportunity for rapid fielding of capabilities to pace threats, the suitability of commercial technologies to meet hard-real-time requirements within a surface combat system is unclear. This research sets to establish technical data to validate the effectiveness and suitability of current commercial technologies to meet the hard-real-time demands of a DoD combat management system. (Moreland Jr., 2013) conducted similar research; however, microservices, containers, and container orchestration technologies were not on the DoD radar at the time. Updated knowledge in this area is desired to inform future DoD roadmaps and investments. A mission-based approach will be used to set the context for applied research. A hypothetical yet operationally relevant Strait Transit scenario has been established to provide context for definition of experimental parameters to be set while assessing the hypothesis. System models and data from a cloud computing environment is used to collect data for quantitative analysis.

## Getting Started using a Docker Container

1. Install and initialize Docker

2. Clone the repository from GitHub into a project directory; e.g. dss-prototype

        cd project-directory
        git pull --rebase

3. We'll use Docker Compose to automatically build and run our containers. However, manual build instructions are included below. 

Ensure that docker compose is installed on the host machine. Navigate the to project main directory and run Docker Compose

        cd project-directory
        docker compose up -d

## The following named container endpoints should now be available

dss-ui:         http://localhost:5000  
tm-server:      http://localhost:3200/docs  
wa-app:         http://localhost:3201/docs  
te-app:         http://localhost:3202/docs
opensky-int:    http://localhost:3203/docs  
test-app:       http://localhost:5150/docs 
  
telem-jaeger:   http://localhost:16686  
grafana:        http://localhost:3000  
notebook:       http://localhost:10000  

-------------------------------------------------------------------------
## Manual build and run process
Docker Compose automatically builds and runs the containers; however, these instructions are provided for manual building and running each application individally.

### DSS-UI Application
Go into the dss-ui-app source code directory and build the container image for the user interface front-end

        docker build --tag dss-ui-app .

Verify new image exists

        docker images

Establish network for containers to connect

        docker network create dss-net

Start the image in detached mode mapping desired port (e.g. 5000) to port 5000 (tbd:5000). Note: The --rm option is included to clear up dependencies automatically when the container is stopped.

        docker run --rm -d -p 5000:5000 --network=dss-net --name=dss-ui dss-ui-app

### Track Management Application
Go into the tm-app source code directory and build the container image for the Track Management application

        docker build --tag tm-app .
        docker images

Start the Track Management server container in detached mode

        docker run --network-alias=tm-server --network=dss-net --name=tm-server --rm -d -p 3200:3200 tm-app

### Weapons Assessment Service Application
Go into the wa-app source code directory and build the container image for the Weapons Assessment service

        docker build --tag wa-app .
        docker images

Start the Threat Evaluation Service Container in detached mode

        docker run --network-alias=wa-app --network=dss-net --name=wa-app --rm -d -p 3201:3201 wa-app


### Trial Engage Service Application
Go into the te-app source code directory and build the container image for the Trial Engage Service

        docker build --tag te-app .
        docker images

Start the Trial Engage Service Container in detached mode

        docker run --network-alias=te-app --network=dss-net --name=te-app --rm -d -p 3202:3202 te-app

### OpenSky Interface
Go into the opensky-int source code directory and build the container image for the OpenSky Interface

        docker build --tag opensky-int .
        docker images

Start the OpenSky Interface Container in detached mode

        docker run --network-alias=opensky-int --network=dss-net --name=opensky-int --rm -d -p 3203:3203 opensky-int


### Jaeger
Jaegar tracing is enabled using collection port 6831. Use the following to start Jaegar in a container in detached mode

        docker run --network-alias=telem-jaeger --network=dss-net --name=jaeger -d -p 16686:16686 -p 6831:6831/udp jaegertracing/all-in-one

### Grafana
Add Grafana to see visualization dashboards and for exporting data via .CSV. The default username and password is admin/admin. You will need to add Jaeger as a data source from http://local-ip-addr:16686

        docker run --network=dss-net --name=grafana --rm -d -p 3000:3000 grafana/grafana

Verify that participants are on the dss-network

        docker network inspect dss-net

### Jupyter Notebook
Add Jupyter Notebook from within the analysis/data directory

        docker run -it --rm -d -p 10000:8888 -v ${PWD}:/home/jovyan/work --name notebook jupyter/r-notebook:latest
        
To find the token from the container:

        docker exec -it notebook jupyter server list

### Test Application
Install and run the automated test application

        docker run  --network=dss-net --name=test-app  --rm -d -p 5150:5150 test-app