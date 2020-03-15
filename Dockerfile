FROM python:3.6

WORKDIR /data/dev/robotjes

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD python ./bin/runpika --env=$RM_ENV
