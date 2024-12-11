web: gunicorn app:app
worker: celery -A celery_setup.celery_config worker -l INFO