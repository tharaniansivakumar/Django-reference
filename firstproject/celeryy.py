import os
# from celery import Celery
from celery import Celery
from firstproject import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'firstproject.settings')

app = Celery('firstproject')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
