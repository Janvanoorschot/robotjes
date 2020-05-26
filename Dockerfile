FROM python:3.8

WORKDIR /data/dev/robotjes

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD python ./bin/simulation_runner --pikaurl=amqp://guest:guest@rabbitmq:5672/%2F
