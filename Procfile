web: gunicorn app:app
worker: celery -A celery_setup.celery_config.celery worker -l INFO