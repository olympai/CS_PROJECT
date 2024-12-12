from kombu import Queue
from celery import Celery
import os

from factory import app
from machine_learning.clustering import clustering_function

# REDIS_KEY = f'{os.environ.get("REDIS_URL")}?ssl_cert_reqs=CERT_NONE'
REDIS_KEY = 'rediss://:p4c33af47ee5e308b34397db785ad1142bbe6e440c30db12a55959c91921fbc86@ec2-52-212-226-188.eu-west-1.compute.amazonaws.com:13040?ssl_cert_reqs=CERT_NONE'

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

# import the tasks
@celery.task(bind=True)
def async_clustering_function(self, session_id):
    with app.app_context():
        clustering_function(session_id)
        self.update_state(state='SUCCESS')
    pass