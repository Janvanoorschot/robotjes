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




ToDo Robotjes: Game UI Development
• create the Model/View/Controller objects and connect them
• 

Model/View/Controller mechanism. 
• Controller -> RoboAdmin
• View -> RoboAdminWindow
• Model -> RoboRequestor

ToDo:

• extend robo_requestor so we can do get and post. Make it generic GTK/request



• create/update Server UI that does the following
∘ on a keypress
‣ create a new game (receive the game-id)
‣ every so often, get a list of games (or automatically)
‣ when game is created
• every often get and display the game state
• when game is closed halt

• create a new Client UI that does the following
∘ every so often, get a list of games and try to register
‣ when registered
• walk through game phases


