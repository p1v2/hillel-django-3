import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hillelDjango3.settings')

app = Celery('hillelDjango3')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'daily_order_count': {
        'task': 'products.tasks.daily_order_count',
        'schedule': crontab(hour='10', minute='0'),
    },
}
