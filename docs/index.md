# Robotjes

Robotjes is a simulation environment where Robomind scripts can be executed. The execution of a script 
results in a Recording. A Recording can be played in a browser.

## Next step

Create a DevIFace, a Runner so we can develop the Engine/Maze/Recorder

DeviIFace is passed to robo so it can use it to implement commands. DevIFace itself gets 
the Runner so it can do a Request/Reply dance with the Runner.

The Runner has a Recorder and a Maze. The latter has a Map.

The last thing to determine is the heartbeat.

## Components

* Map
* Maze
* Engine
* Recorder
* Player
* Runner

