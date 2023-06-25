FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

COPY ./app /app
RUN pip install --upgrade pip && apk add py-cryptography
RUN pip install -r /app/requirements.txt
