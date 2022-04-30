from celery import Celery
from celery.schedules import crontab

app = Celery("news", broker="amqp://",
             backend="rpc://", include=["news.task"])

app.conf.update(
    result_expires=3600
)
# celery scheduled job set up
# Currently hard-coded, next will be fetching urls from db.

app.conf.beat_schedule = {
    "run_news": {
        "task": "news.task.allNews",
        "schedule": crontab(minute=0, hour="*/6"),
        # "schedule": 60,
        "args": ([
            ["https://www.reuters.com", "https://www.bbc.com/news",
                "https://edition.cnn.com", "https://finviz.com"],
            ["business", "world"]
        ])
    }
}
app.conf.timezone = 'Asia/Hong_Kong'

if __name__ == "__main__":
    app.start()

#
