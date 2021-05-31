## Haiti MSPP application

Application to manage the MSPP fundings of Haiti


## Key Python modules and tools used

- [Flask](https://flask.palletsprojects.com/): Flask is a lightweight WSGI web application framework. It is designed to make getting started quick and easy, with the ability to scale up to complex applications.
- [Flask-RESTful](https://flask-restful.readthedocs.io): Extension for Flask that adds support for quickly building REST APIs
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io): Adds support for using JSON Web Tokens (JWT) to Flask for protecting views
- [Docker](https://docs.docker.com/get-started/overview/): Docker is an open platform for developing, shipping, and running applications.


## Quick guide to get started

Clone the repository:

```sh
$ git clone https://github.com/daencordova/haiti-mspp.git
$ cd haiti-mspp
```

Rename *.env.example* to *.env* to run in development and update the environment variables.

- `SECRET_KEY=<secret_key>`
- `JWT_SECRET_KEY=<jwt_secret_key>`
- `POSTGRES_USER=<postgres_user>`
- `POSTGRES_PASSWORD=<postgres_pass>`
 
 Build the images and run the containers:

```sh
$ docker-compose up --build -d
$ docker-compose exec api python manage.py create-db
$ docker-compose exec api python manage.py seed-db
$ docker-compose exec db psql --username=<pg_username> --dbname=haiti_mspp
$ docker-compose exec api flake8 .
$ docker-compose exec api black .
```

Test it out at [http://0.0.0.0:5000/docs](http://0.0.0.0:5000/docs)

Stop running containers

```sh
$ docker-compose down
```

