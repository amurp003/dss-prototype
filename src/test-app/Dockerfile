# syntax=docker/dockerfile:1
# https://fastapi.tiangolo.com/deployment/docker/

FROM python:3.8-slim-buster

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/app

CMD [ "uvicorn", "app.test-app:app" , "--host", "0.0.0.0", "--port", "5150"]

