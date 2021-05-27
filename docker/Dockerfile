FROM python:3.8

RUN apt-get update -y

RUN mkdir /work && mkdir /work/data

WORKDIR /work

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt
