# labs.robomindacademy.com Installation

### Docker Registry Server

The docker swarm requires it own Docker Registry Server from which the images for robomind/robo and
robomind/robotjes are served.

So first we create the images and the registry in which we will store them:

```bash
docker build -f ./Dockerfile-robo -t robomind/robo:1.0 .
docker build -f ./Dockerfile -t robomind/robotjes:1.0 .
docker run -d   -p 5000:5000   --restart=always   --name registry   registry:2
```

Next we store the images in the registry:

```bash
docker tag robomind/robotjes:1.0 localhost:5000/robomind/robotjes:1.0
docker push localhost:5000/robomind/robotjes:1.0
docker tag robomind/robo:1.0 localhost:5000/robomind/robo:1.0
docker push localhost:5000/robomind/robo:1.0
```

And to deploy/view/remove the stack in the swarm:

```bash
docker stack deploy --compose-file labs-swarm.yml roboswarm
docker stack services roboswarm
docker stack rm roboswarm
```


