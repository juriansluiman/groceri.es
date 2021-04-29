FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

RUN pip install --upgrade pip

RUN apk add --no-cache \
        gcc \
        libressl-dev \
        musl-dev \
        libffi-dev && \
    pip install --no-cache-dir cryptography==2.1.4 && \
    apk del \
        gcc \
        libressl-dev \
        musl-dev \
        libffi-dev

COPY ./app/requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY ./app /app
