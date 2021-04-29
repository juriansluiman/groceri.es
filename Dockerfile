FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

RUN pip install --upgrade pip

RUN apk add py-cryptography

COPY ./app/requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY ./app /app
