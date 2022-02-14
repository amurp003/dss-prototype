# Decision Support System (DSS) Microservices Project

The United States Department of Defense (DoD) is rapidly working with DoD Services to move from multi-year (e.g. 7-10) traditional acquisition programs to a commercial industry-based approach for software development. While commercial technologies and approaches provide an opportunity for rapid fielding of capabilities to pace threats, the suitability of commercial technologies to meet hard-real-time requirements within a surface combat system is unclear. This research sets to establish technical data to validate the effectiveness and suitability of current commercial technologies to meet the hard-real-time demands of a DoD combat management system. (Moreland Jr., 2013) conducted similar research; however, microservices, containers, and container orchestration technologies were not on the DoD radar at the time. Updated knowledge in this area is desired to inform future DoD roadmaps and investments. A mission-based approach will be used to set the context for applied research. A hypothetical yet operationally relevant Strait Transit scenario has been established to provide context for definition of experimental parameters to be set while assessing the hypothesis. System models and data from a cloud computing environment is used to collect data for quantitative analysis.

## Getting Started using a Docker Container

1. Install and initialize Docker

2. Clone the repository from GitHub into a project directory

3. Build the container image

        docker build --tag dss-prototype .

4. Verify new image exists

        docker images

5. Start the image in detached mode mapping desired port (e.g. 5000) to port 5000 (tbd:5000)

        docker run -d -p 5000:5000 dss-prototype

6. Jaegar tracing is currently enabled using collectin port 6831. Use the following to start Jaegar in a container

        docker run -p 16686:16686 -p 6831:6831/udp jaegertracing/all-in-one
