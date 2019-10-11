# Tennis friends #

# To start app #
`python manage.py createmigrations app`
`python manage.py migrate`
`python manage.py createsuperuser`

## Docker ##
Build docker image: `docker build . --tag "tennis:1.0"`
Run docker image `docker run -p 8000:8000 -i -t <ID>`
Or use `docker-compose`: `docker-compose up --build`

For proper DB work set in docker container env for DB host: `DB_HOST=host.docker.internal`
For Mac add static folder and `nginx/conf` to `Preferences -> File Sharing`