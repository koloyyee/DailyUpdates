from celery import Celery
from celery.schedules import crontab

app = Celery("news", broker="amqp://",
             backend="rpc://", include=["news.task"])

app.conf.update(
    result_expires=3600
)

app.conf.beat_schedule = {
    'run_cnn': {
        'task': 'news.task.cnn',
        'schedule': crontab(hour=6, minute=45),
        'args': (["business", "world"],),
    },
    'run_bbc': {
        'task': 'news.task.bbc',
        'schedule': crontab(hour=6, minute=45),
        'args': (["business", "world"],),
    },
    'run_finviz': {
        'task': 'news.task.finviz',
        'schedule': crontab(hour=6, minute=45),
    },

}
app.conf.timezone = 'Asia/Hong_Kong'

if __name__ == "__main__":
    app.start()

# To run a celery task
# celery -A {name of the app} worker -l INFO

# To run celery beat
# celery -A {name of the app} beat

# To run celery tasks on the background we can use
# celery multi start w1 -A proj -l INFO

# To restart
# celery multi restart w1 -A proj -l INFO

# To stop
# celery multi stop w1 -A proj -l INFO

# Async stop
# celery multi stopwait w1 -A proj -l INFO

# start a node
# rabbitmq-server start

# start a node behind the scene
# rabbitmq-server -detached

# stop a node
# rabbitmqctl stop
