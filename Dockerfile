FROM python:3.8

RUN apt update && apt install -y --no-install-recommends \
	        libgirepository1.0-dev \
	        libcairo2-dev \
	        python3-dev \
	    && rm -rf /var/lib/apt/lists/*

WORKDIR /data/dev/robotjes

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD python ./bin/simulation_runner --pikaurl=amqp://guest:guest@rabbitmq:5672/%2F
