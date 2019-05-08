# Property Management company website

This is a website I created during my internship in a local based property management company. Project uses Python, Django, PostgreSQL, Celery, and Redis as a cache engine and a message broker.

## Installation

Clone the perository

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

```bash
pip install -r requirements.txt
```
Change database settings in 'settings.py'

Install [Redis](https://redis.io/) (for Ubuntu based systems just type):

```bash
sudo apt install redis
```
Then we need to check if the redis server works or not. First, open redis command line interface by typing:
```bash
redis-cli
```
Then, type PING and press Enter. if the result is
```bash
PONG
```
then everything is ok.

Create tables in a database by typing:
```bash
python manage.py migrate
```
Collect static files:
```bash
python manage.py collectstatic
```
Run a wsgi server by typing:
```bash
python manage.py runserver
```
The server runs automatically on 127.0.0.1:8000

## Built With


* [Python](http://python.org) - programming language

* [Django](https://www.djangoproject.com/) - Django web framework

* [Redis](https://redis.io/) - A NoSQL database and a message broker

* [Celery](http://www.celeryproject.org/) - A background task manager
## Contributing

Any changes are welcome.

## License
MIT
