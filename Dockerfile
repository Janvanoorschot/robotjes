FROM python:3.8
ARG PIKA_URL
ENV PIKA_URL=$PIKA_URL

RUN apt update && apt install -y --no-install-recommends \
	    && rm -rf /var/lib/apt/lists/*
#RUN apt update && apt install -y --no-install-recommends \
#            python3-pip \
#	        libgirepository1.0-dev \
#	        libcairo2-dev \
#	        python3-dev \
#	    && rm -rf /var/lib/apt/lists/*

#WORKDIR /data/dev/robotjes

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD python ./bin/simulation_runner --pikaurl=$PIKA_URL
