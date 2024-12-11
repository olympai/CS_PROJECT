from kombu import Queue
from celery import Celery
import os

from factory import app

REDIS_KEY = f'{os.environ.get("REDIS_TLS_URL")}?ssl_cert_reqs=CERT_NONE'

# create celery app (asynchronous backend)
def create_celery_app(flask_app):
    celery = Celery(
        'app',  # Geben Sie hier einen eindeutigen Namen für Ihre Celery-App an
        backend=REDIS_KEY,
        broker=REDIS_KEY,  # Geben Sie die Broker-URL an (hier wird RabbitMQ als Beispiel verwendet)
        broker_connection_retry_on_startup=True
    )
    celery.conf.update(flask_app.config)
    # sample queue configuration, only one for this environment
    celery.conf.task_queues = (
        Queue('alpha', routing_key='alpha'),
    )
    return celery

celery = create_celery_app(app)