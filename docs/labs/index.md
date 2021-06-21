# Setup Labs

## Hardware

The Robomind Academy development environment 'labs.robomindacadem.com' consists of a
headend server with a stack of Raspberry Pi 4's behind it. 

### labs: Headend server

This Ubuntu server acts as headend for web traffic and runs the following software:

* A NGINX server that (amongst other duties) servers static content for labs

### rapsie0: Queen raspie
This ubuntu server running in a Docker swarm 'roboswarm' and acts as local headend. It runs:

* Postgresql Database
* RabbitMQ server
* RMG grails web-application

### raspie1-4: Worker raspies
This stack of ubuntu server Raspberry Pi 4's behind it run:
  
* n* robomnind/robo container
* m* robomind/robotjes container

## Software
The whole of the Robomind Academy is contained in the following GIT repositories:

* [The core Robomind Academy (rmg) **private**](https://github.com/Janvanoorschot/robomindacademy)
* [The Puppeteer for the robomind workers executing scripts](https://github.com/Janvanoorschot/robotjes)
* [The client code for Robomind scripts](https://github.com/Janvanoorschot/robotjes-client)
* [The core Robomind courses](https://github.com/Janvanoorschot/robocontent)
* [The Python course **private**](https://github.com/Janvanoorschot/robopython)
* [Robomind Academy usage analysis software **private**](https://github.com/Janvanoorschot/anarobo)
* [Selenium software to stress test Robomind Academy](https://github.com/Janvanoorschot/roboselenium)
* [Viewer of Robomind Academy activity counters **private**](https://github.com/Janvanoorschot/viewrobo)



