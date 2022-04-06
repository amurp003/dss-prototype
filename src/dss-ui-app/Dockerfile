# syntax=docker/dockerfile:1

FROM python:3.9

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app/

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]