import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_vms.settings')

app = Celery('core_vms')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
