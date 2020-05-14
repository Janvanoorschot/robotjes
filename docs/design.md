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
* client: PyGObject/GTK UI/Windows/Graphics library
* client: WebKit component for browser in GTK/Python
* client: Requests for REST calls (in seperate thread with callbacks, no asyncio in UI)

### Client Components
* C1: viewer
* C2: solution runner
* S2: bubble manager

### Server Components
* S1[roborest]: REST implementation server
* S2[bubbles]: bubble server (RabbitMQ)
* S3[runner]: bubble runner containing simulation and player nodes (RabbitMQ)

## Roadmap
1. S1: FastAPI based REST server embedded in Uvicorn
2. C3: PyGObject based talker to REST server (dummy content)






