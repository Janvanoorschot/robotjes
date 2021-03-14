# FROM python:3.8
FROM python:3.8-slim-buster
ARG PIKA_URL
ENV PIKA_URL=$PIKA_URL

RUN apt update && apt install -y --no-install-recommends \
        libpq-dev \
        build-essential \
	    && rm -rf /var/lib/apt/lists/*

RUN addgroup   --system --gid 6161 robo
RUN adduser  --system --uid  6161  --group robo
USER robo

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD python ./bin/simulation_runner --pikaurl=$PIKA_URL
