# The Robomind Academy Recording, Reversed Engineerd

A recording is an array of keyFrames, dictionaries with the following
content:

* 'sprite': always 'r', probably short for 'robot'
* 'action': array where the first element is the action and the rest args
* 'src': the source-line 
* 'score': seems to be the accumulated score until that keyframe

An example of such a keyframe is:
```json
      {
        "sprite": "r",
        "action": [
          "f",
          "0",
          "1"
        ],
        "src": 6,
        "score": 6
      }
```

In order to get an idea of the handling of a keyFrame look at 
frameplayer.js/doNextCommand. 