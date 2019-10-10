FROM python:3.6.5

MAINTAINER AlexKotl

# Copy the application folder inside the container
ADD . /usr/src/app

# set the default directory where CMD will execute
WORKDIR /usr/src/app

RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

# Expose ports
EXPOSE 8000

CMD exec gunicorn app.wsgi:application --bind 0.0.0.0:8000 --workers 3
