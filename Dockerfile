# FROM python:3.8
FROM python:3.8-slim-buster
ARG PIKA_URL
ENV PIKA_URL=$PIKA_URL

RUN apt update && apt install -y --no-install-recommends \
	    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD python ./bin/simulation_runner --pikaurl=$PIKA_URL
