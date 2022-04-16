# DailyUpdates

Daily news aggregator for top 20 headlines from BBC, CNN, Finviz, or any of your choice.

## Practice

This is repo uses Python,
the main idea is to practice Python through projects, it allow me to explore different packages and library,
this is based on the flask 2.x tutorial, it is a very good guide on development.

## Packages

In this project, I have used Flask, urllib3, beautifulsoup4, celery, rabbitmq, sqlite3

## Current

Currently, it allows us to fetch news from BBC, CNN, and Finviz, and show the top 20 accordingly.

## Future

More flexbility on which news agency, the website or even a login system.

if you woud like to try on your own you can folk it then

```bash
# after downloading, create virutal env
cd DailyUpdates
python -m venv venv
source venv/bin/activate

# install packagaes
pip install

# set up dev environment for flask
export FLASK_APP=dailyUpdates
export FLASK_ENV=development

# initialize sqlite db
flask initDB

# run flask app in default (:5000)
flask run
```

More updates coming up

### RabbitMQ and Celery scheduled job command

```bash
# To run a celery task
celery -A {name of the app} worker -l INFO

# To run celery beat
celery -A {name of the app} beat

# To run celery tasks on the background we can use
celery multi start w1 -A proj -l INFO

# To restart
celery multi restart w1 -A proj -l INFO

# To stop
celery multi stop w1 -A proj -l INFO

# Async stop
celery multi stopwait w1 -A proj -l INFO

# start a node
rabbitmq-server start

# start a node behind the scene
rabbitmq-server -detached

# stop a node
rabbitmqctl stop
```
