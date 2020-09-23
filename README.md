## drf - Book My Ticket

### Overview

##### "Book My Show"-like rest APIs implementation using Django-rest-framework. 

### Technologies Used (Top Level):
1. Django (3.1.1)
2. Django Rest Framework (3.11.1)
3. Docker
4. PostgresSQL

### Features

* Test Coverage - Included model and views tests using django [TestCase](https://docs.djangoproject.com/en/3.1/topics/testing/overview/#writing-tests) and DRF [APITestCase](https://www.django-rest-framework.org/api-guide/testing/#api-test-cases) respectively.
* Swagger Docs - Out of the box API documentation using [drf-yasg](https://drf-yasg.readthedocs.io/en/stable/readme.html#features). 
* Logging - Request/Response logging along with metadata to console.
* Docker - Fully containerized application, provides python-alpine 3.8, DRF dependencies and PostgresSQL configured. [docker-compose](https://github.com/jgrt/drf-book-my-ticket/blob/master/docker-compose.yml) for local development.

### Getting Started
* If you wish to run your own build, first ensure you have docker running in your local machine.
if not, first get docker [here](https://docs.docker.com/get-docker/).

* Then, clone this repo to your machine
```
$ git clone https://github.com/jgrt/drf-book-my-ticket.git
```
* after cloning repo, run following commands to build and start services defined in [docker-compose.yml](https://github.com/jgrt/drf-book-my-ticket/blob/master/docker-compose.yml)
```
$ docker-compose build
$ docker-compose up web
``` 

If everything goes right you have running django app on port (default 80), visit at localhost

To make migrations, you need to go inside docker web service
```
docker-compose exec web bash
```

* then, run few more commands to migrate and sync to database
```
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
```

##### Finally
You can now access the swagger on your browser by using and test APIs,
```
http://localhost/swagger/
```
