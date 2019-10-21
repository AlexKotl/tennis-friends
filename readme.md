# Tennis friends #

This website was created to help tennis players find partners for the game.
Built with Python + Django, Mysql, Bootstrap 4, Docker.

## Starting app ##
- `python manage.py createmigrations app`
- `python manage.py migrate`
- `python manage.py createsuperuser`

Start with Gunicorn: `gunicorn app.wsgi:application --bind 0.0.0.0:8000 --workers 3`

## Docker ##
- Build docker image: `docker build . --tag "tennis:1.0"`
- Run docker image `docker run -p 8000:8000 -i -t <ID>`

Or use Docker Compose: `docker-compose up --build`

For proper DB work set in docker container env for DB host: `DB_HOST=host.docker.internal`

For Mac: add `static`, `app` and `nginx` folders to `Preferences -> File Sharing` of Docker.

Run commands inside Docker: `docker exec -it <mycontainer> bash`