FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

RUN pip install --upgrade pip && apk add py-cryptography
COPY ./app /app
RUN pip install -r /app/requirements.txt
