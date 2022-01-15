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
```
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
