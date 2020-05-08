# Design
So we are going to create a GTK app which uses Webkit as viewer.

Server-side we will use FastAPI with Uvicorn to receive all kind of commands:
* create a bubble
* register with a bubble
* start  a bubble
* command to a bubble

The server-side communicates via RabbitMQ with the bubble-runner, which in
turn talks to a simulation.

## Libraries
* server: Uvicorn: http server
* server: FastAPI: REST library
* server: AIO-pika: interface to RabbitMQ
* client: GTK UI/Windows/Graphics library
* client: WebKit browser in GTK/Python

## Components
* client: viewer
* client: solution runner
* client: bubble manager
* server: REST implementation server
* server: bubble runner
* server: robo simulation



