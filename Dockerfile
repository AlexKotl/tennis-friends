FROM python:3.6.5

MAINTAINER AlexKotl

ADD . /data
WORKDIR /data

RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

EXPOSE 8000

CMD exec gunicorn app.wsgi:application --bind 0.0.0.0:8000 --workers 3
