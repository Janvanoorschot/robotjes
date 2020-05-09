# Design
So we are going to create a GTK app which uses Webkit as viewer.

Server-side we will use FastAPI with Uvicorn to receive all kind of commands:
* create a bubble
* register with a bubble
* start  a bubble
* command to a bubble

The server-side communicates via RabbitMQ with the bubble-runner, which in
turn talks to a simulation.

## Components

### Libraries
* server: Uvicorn: http server
* server: FastAPI: REST library
* server: AIO-pika: interface to RabbitMQ
* client: PyGObject UI/Windows/Graphics library
* client: WebKit component for browser in GTK/Python

### Client Components
* viewer
* solution runner
* bubble manager

### Server Components
* REST implementation server
* bubble runner containing simulation and player nodes

## Roadmap




