FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7

RUN pip install --upgrade pip

COPY ./app/requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY ./app /app
