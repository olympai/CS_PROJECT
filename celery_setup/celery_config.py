from kombu import Queue
from celery import Celery
import os

from factory import app

REDIS_KEY = f'{os.environ.get("REDIS_URL")}?ssl_cert_reqs=CERT_NONE'

# create celery app (asynchronous backend)
def create_celery_app(flask_app):
    celery = Celery(
        'app', 
        backend=REDIS_KEY,
        broker=REDIS_KEY, 
        broker_connection_retry_on_startup=True
    )
    celery.conf.update(flask_app.config)
    # sample queue configuration, only one for this environment
    celery.conf.task_queues = (
        Queue('alpha', routing_key='alpha'),
    )
    return celery

celery = create_celery_app(app)