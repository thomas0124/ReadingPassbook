FROM python:3.9

WORKDIR /app

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y libgl1-mesa-dev
RUN apt-get install -y libzbar0

RUN pip install pyzbar

COPY . /app